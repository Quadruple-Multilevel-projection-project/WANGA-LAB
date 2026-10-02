from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Mapping, Sequence, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


THREE_D = 3
SIX_D = 6
FIVE_D = 5
CONCEPT_SLOTS = 175
HEXA_COMPLEX_COUNT = 6
EVOLUTION_LAYERS = 10


class LogicPillar(str, Enum):
    CLASSICAL_PREDICATE = "CLASSICAL_PREDICATE"
    MODAL_TEMPORAL = "MODAL_TEMPORAL"
    INTUITIONISTIC = "INTUITIONISTIC"
    HIGHER_ORDER_TYPE = "HIGHER_ORDER_TYPE"
    MANY_VALUED_STRUCTURAL = "MANY_VALUED_STRUCTURAL"
    PARACONSISTENT = "PARACONSISTENT"


@dataclass(frozen=True)
class DriftGrid6D:
    """Six control axes used as active structural controls.

    The values are control variables for the computational model. They are
    not asserted to be physical coordinates.
    """

    alpha: float
    beta: float
    gamma: float
    delta: float
    epsilon: float
    zeta: float

    def as_tensor(self, *, dtype=torch.float32, device=None) -> torch.Tensor:
        return torch.tensor(
            [
                self.alpha,
                self.beta,
                self.gamma,
                self.delta,
                self.epsilon,
                self.zeta,
            ],
            dtype=dtype,
            device=device,
        )


@dataclass(frozen=True)
class StructuralNode:
    node_id: int
    position_xyz: Tuple[float, float, float]

    def tensor(self, *, dtype=torch.float32, device=None) -> torch.Tensor:
        return torch.tensor(self.position_xyz, dtype=dtype, device=device)


@dataclass(frozen=True)
class StructuralUpdate:
    node_id: int
    old_position: Tuple[float, float, float]
    correction: Tuple[float, float, float]
    new_position: Tuple[float, float, float]
    logical_distance: float
    geometric_distance: float
    drift_norm: float

    def as_dict(self) -> Dict[str, object]:
        return {
            "node_id": self.node_id,
            "old_position": list(self.old_position),
            "correction": list(self.correction),
            "new_position": list(self.new_position),
            "logical_distance": self.logical_distance,
            "geometric_distance": self.geometric_distance,
            "drift_norm": self.drift_norm,
        }


def deterministic_structural_update(
    *,
    node: StructuralNode,
    reference: StructuralNode,
    logical_distance: float,
    drift: DriftGrid6D,
    logical_gain: float = 1.0,
    drift_gain: float = 0.1,
) -> StructuralUpdate:
    """Apply a deterministic structural update contract.

    The direction comes from the current geometry; the magnitude couples the
    supplied formal logical distance with the six-axis control field.

    This is an executable structural law, not a physical constitutive law.
    """

    p_i = node.tensor()
    p_j = reference.tensor()
    delta = p_j - p_i
    geometric_distance = float(torch.linalg.vector_norm(delta).item())

    if geometric_distance > 1e-12:
        unit = delta / geometric_distance
    else:
        unit = torch.zeros(THREE_D)

    drift_tensor = drift.as_tensor()
    drift_projection = torch.tensor(
        [
            drift_tensor[0] - drift_tensor[1],
            drift_tensor[2] - drift_tensor[3],
            drift_tensor[4] - drift_tensor[5],
        ],
        dtype=torch.float32,
    )

    mismatch = logical_gain * (logical_distance - geometric_distance)
    correction = mismatch * unit + drift_gain * drift_projection

    new_position = p_i + correction

    return StructuralUpdate(
        node_id=node.node_id,
        old_position=tuple(float(x) for x in p_i.tolist()),
        correction=tuple(float(x) for x in correction.tolist()),
        new_position=tuple(float(x) for x in new_position.tolist()),
        logical_distance=float(logical_distance),
        geometric_distance=geometric_distance,
        drift_norm=float(torch.linalg.vector_norm(drift_tensor).item()),
    )


class TiedWeightAdaptiveNeuron(nn.Module):
    """3-in-1 neuron: encode, tied-weight reconstruct, and drift monitor."""

    def __init__(self, input_dim: int, hidden_dim: int):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim, bias=True)
        self.output_bias = nn.Parameter(torch.zeros(input_dim))

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        return torch.tanh(self.encoder(x))

    def reconstruct(self, h: torch.Tensor) -> torch.Tensor:
        weight = self.encoder.weight
        return torch.tanh(F.linear(h, weight.transpose(0, 1), self.output_bias))

    def forward(
        self,
        x: torch.Tensor,
        drift_threshold: float,
    ) -> Dict[str, torch.Tensor | bool]:
        h = self.encode(x)
        x_hat = self.reconstruct(h)
        error = torch.mean((x - x_hat) ** 2)
        stable = bool(error.detach().item() <= drift_threshold)

        return {
            "hidden": h,
            "reconstruction": x_hat,
            "reconstruction_error": error,
            "stable": stable,
        }


class HyperNeuron(nn.Module):
    """Dynamic weight generator driven by a drift/error state.

    It generates a new candidate weight tensor in one forward pass. Applying
    that candidate is explicit and caller-controlled.
    """

    def __init__(self, state_dim: int, weight_shape: Tuple[int, int]):
        super().__init__()
        self.weight_shape = weight_shape
        flat_size = weight_shape[0] * weight_shape[1]
        self.generator = nn.Sequential(
            nn.Linear(state_dim, max(32, flat_size // 2)),
            nn.Tanh(),
            nn.Linear(max(32, flat_size // 2), flat_size),
        )

    def generate(self, drift_state: torch.Tensor) -> torch.Tensor:
        if drift_state.shape[-1] != self.generator[0].in_features:
            raise ValueError("drift_state has incompatible feature dimension")
        flat = self.generator(drift_state)
        return flat.reshape(*self.weight_shape)

    def apply_to(self, module: nn.Linear, drift_state: torch.Tensor) -> torch.Tensor:
        candidate = self.generate(drift_state)
        if tuple(module.weight.shape) != self.weight_shape:
            raise ValueError("target module weight shape does not match hyper-neuron")
        with torch.no_grad():
            module.weight.copy_(candidate)
        return candidate


@dataclass
class HexaComplex:
    complex_id: int
    order: str
    pillars: Tuple[LogicPillar, LogicPillar, LogicPillar]

    def __post_init__(self) -> None:
        if self.order not in {"FOL", "SOL"}:
            raise ValueError("order must be FOL or SOL")
        if len(self.pillars) != 3:
            raise ValueError("Each hexa-complex must have exactly 3 pillars.")

    def as_dict(self) -> Dict[str, object]:
        return {
            "complex_id": self.complex_id,
            "order": self.order,
            "pillars": [p.value for p in self.pillars],
        }


def build_hexa_complexes() -> Tuple[HexaComplex, ...]:
    """3 FOL + 3 SOL complexes sharing the six formal logic pillars."""

    return (
        HexaComplex(
            1,
            "FOL",
            (
                LogicPillar.CLASSICAL_PREDICATE,
                LogicPillar.MODAL_TEMPORAL,
                LogicPillar.INTUITIONISTIC,
            ),
        ),
        HexaComplex(
            2,
            "FOL",
            (
                LogicPillar.CLASSICAL_PREDICATE,
                LogicPillar.INTUITIONISTIC,
                LogicPillar.MODAL_TEMPORAL,
            ),
        ),
        HexaComplex(
            3,
            "FOL",
            (
                LogicPillar.INTUITIONISTIC,
                LogicPillar.CLASSICAL_PREDICATE,
                LogicPillar.MODAL_TEMPORAL,
            ),
        ),
        HexaComplex(
            4,
            "SOL",
            (
                LogicPillar.HIGHER_ORDER_TYPE,
                LogicPillar.MANY_VALUED_STRUCTURAL,
                LogicPillar.PARACONSISTENT,
            ),
        ),
        HexaComplex(
            5,
            "SOL",
            (
                LogicPillar.MANY_VALUED_STRUCTURAL,
                LogicPillar.PARACONSISTENT,
                LogicPillar.HIGHER_ORDER_TYPE,
            ),
        ),
        HexaComplex(
            6,
            "SOL",
            (
                LogicPillar.PARACONSISTENT,
                LogicPillar.HIGHER_ORDER_TYPE,
                LogicPillar.MANY_VALUED_STRUCTURAL,
            ),
        ),
    )


class DeterministicSatisfiabilityConsensus:
    """Execution-time discrete consensus layer.

    Continuous scores may exist upstream during training, but the consensus
    output is a deterministic decision over fixed predicates and constraints.
    """

    def decide(
        self,
        *,
        conditions: Mapping[str, bool],
        priorities: Sequence[str],
    ) -> Dict[str, object]:
        satisfied = [name for name in priorities if bool(conditions.get(name, False))]
        selected = satisfied[0] if satisfied else None

        return {
            "satisfied": satisfied,
            "selected": selected,
            "is_consistent": len(satisfied) > 0,
            "condition_count": len(conditions),
        }


__all__ = [
    "CONCEPT_SLOTS",
    "EVOLUTION_LAYERS",
    "DriftGrid6D",
    "StructuralNode",
    "StructuralUpdate",
    "deterministic_structural_update",
    "TiedWeightAdaptiveNeuron",
    "HyperNeuron",
    "HexaComplex",
    "LogicPillar",
    "build_hexa_complexes",
    "DeterministicSatisfiabilityConsensus",
]
