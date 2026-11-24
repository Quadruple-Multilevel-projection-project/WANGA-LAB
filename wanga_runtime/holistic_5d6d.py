from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Sequence, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .reversible_router import (
    OUTER_GATE_COUNT,
    SPACE_GROUP_COUNT,
    ReversibleCombinatorialRouter,
)
from .tziruf_manifold import DynamicNameConfiguration


FIVE_D = 5
SIX_D = 6
CONCEPT_SLOTS = 175
LOGIC_GATES = 14


@dataclass(frozen=True)
class GateDirection:
    gate_id: int
    pair_index_a: int
    pair_index_b: int
    vector_5d: Tuple[float, float, float, float, float]

    def as_dict(self) -> Dict[str, object]:
        return {
            "gate_id": self.gate_id,
            "pair_index_a": self.pair_index_a,
            "pair_index_b": self.pair_index_b,
            "vector_5d": list(self.vector_5d),
        }


def build_231_gate_directions() -> Tuple[GateDirection, ...]:
    """Deterministic algebraic directions for all 231 unordered letter gates.

    The vector is an addressing operator derived from the two alphabet indices.
    It is not a physical force vector and does not encode a claimed
    crystallographic operation.
    """

    gates: List[GateDirection] = []
    gate_id = 1

    for a in range(22):
        for b in range(a + 1, 22):
            s = a + b + 1
            d = b - a
            p = (a + 1) * (b + 1)

            vector = (
                (a - 10.5) / 10.5,
                (b - 10.5) / 10.5,
                (d - 1.0) / 20.0,
                (s - 2.0) / 41.0,
                (p - 2.0) / 440.0,
            )

            norm = sum(x * x for x in vector) ** 0.5
            normalized = tuple(x / max(norm, 1e-8) for x in vector)

            gates.append(
                GateDirection(
                    gate_id=gate_id,
                    pair_index_a=a,
                    pair_index_b=b,
                    vector_5d=normalized,
                )
            )
            gate_id += 1

    if len(gates) != OUTER_GATE_COUNT:
        raise RuntimeError(f"Expected {OUTER_GATE_COUNT} gates, got {len(gates)}.")

    return tuple(gates)


class TorsionalProjection(nn.Module):
    """Maps a six-component control/drift state back into the 5D logic field."""

    def __init__(self) -> None:
        super().__init__()
        self.matrix = nn.Parameter(torch.eye(FIVE_D, SIX_D) * 0.05)

    def forward(self, drift_6d: torch.Tensor) -> torch.Tensor:
        if drift_6d.shape[-1] != SIX_D:
            raise ValueError("drift_6d must end with dimension 6")
        return drift_6d @ self.matrix.transpose(0, 1)


class TorsionLayer(nn.Module):
    """One of the ten nested N-level evolution operators."""

    def __init__(self, index: int, dim: int = 16):
        super().__init__()
        if not 1 <= index <= 10:
            raise ValueError("layer index must be in 1..10")

        self.index = index
        self.linear = nn.Linear(dim, dim, bias=False)
        self.norm = nn.LayerNorm(dim)
        self.torsion_head = nn.Linear(dim, SIX_D, bias=False)

        with torch.no_grad():
            self.linear.weight.copy_(torch.eye(dim))

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        proposal = self.linear(state)
        next_state = self.norm(state + proposal)
        drift = self.torsion_head(next_state)
        return next_state, drift


class DistributedFractalGraphLayer(nn.Module):
    """Layer 6: distributed ring/fractal graph over currently active concepts.

    The graph is a configuration over existing concept IDs, not a new neuron
    allocation. At each recursion depth, a ring connects the selected nodes.
    """

    def __init__(self, dim: int = 16):
        super().__init__()
        self.message = nn.Linear(dim, dim, bias=False)

    @staticmethod
    def ring_adjacency(node_count: int, device: torch.device | None = None) -> torch.Tensor:
        if node_count <= 0:
            return torch.zeros((0, 0), device=device)

        adjacency = torch.zeros((node_count, node_count), device=device)
        if node_count == 1:
            return adjacency

        for i in range(node_count):
            adjacency[i, (i - 1) % node_count] = 1.0
            adjacency[i, (i + 1) % node_count] = 1.0

        return adjacency

    def forward(
        self,
        states: torch.Tensor,
        depths: int = 2,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if states.ndim != 2:
            raise ValueError("states must have shape [nodes, dim]")

        h = states
        total_edge_energy = torch.zeros((), device=states.device, dtype=states.dtype)

        for depth in range(max(1, depths)):
            adjacency = self.ring_adjacency(h.shape[0], h.device)
            degree = adjacency.sum(dim=-1, keepdim=True).clamp_min(1.0)
            aggregated = (adjacency @ h) / degree

            h = h + (0.5 ** (depth + 1)) * self.message(aggregated)
            total_edge_energy = total_edge_energy + torch.mean(
                (h - aggregated) ** 2
            )

        return h, total_edge_energy


class MetaLogicalLoss(nn.Module):
    """Composite objective tying reconstruction, logic, topology and drift."""

    def __init__(
        self,
        lambda_reconstruction: float = 1.0,
        lambda_logic: float = 1.0,
        lambda_torsion: float = 0.25,
        lambda_drift: float = 0.50,
        lambda_topology: float = 0.25,
        lambda_cycle: float = 0.50,
    ):
        super().__init__()
        self.weights = {
            "reconstruction": lambda_reconstruction,
            "logic": lambda_logic,
            "torsion": lambda_torsion,
            "drift": lambda_drift,
            "topology": lambda_topology,
            "cycle": lambda_cycle,
        }

    def forward(
        self,
        source: torch.Tensor,
        reconstruction: torch.Tensor,
        logic_logits: torch.Tensor,
        target_gate: int,
        torsion_6d: torch.Tensor,
        drift_thresholds: torch.Tensor,
        topology_error: torch.Tensor,
        cycle_error: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:

        reconstruction_loss = F.mse_loss(reconstruction, source)

        gate_target = torch.tensor(
            [target_gate - 1],
            dtype=torch.long,
            device=logic_logits.device,
        )
        logic_loss = F.cross_entropy(logic_logits.unsqueeze(0), gate_target)

        torsion_loss = torch.mean(torsion_6d ** 2)

        excess_drift = F.relu(torch.abs(torsion_6d) - drift_thresholds)
        drift_loss = torch.mean(excess_drift ** 2)

        total = (
            self.weights["reconstruction"] * reconstruction_loss
            + self.weights["logic"] * logic_loss
            + self.weights["torsion"] * torsion_loss
            + self.weights["drift"] * drift_loss
            + self.weights["topology"] * topology_error
            + self.weights["cycle"] * cycle_error
        )

        return {
            "total": total,
            "reconstruction": reconstruction_loss,
            "logic": logic_loss,
            "torsion": torsion_loss,
            "drift": drift_loss,
            "topology": topology_error,
            "cycle": cycle_error,
        }


class Holistic5D6DNetwork(nn.Module):
    """Unified executable model for the supplied 5D/6D architecture."""

    def __init__(self, dim: int = 16):
        super().__init__()
        self.dim = dim
        self.router = ReversibleCombinatorialRouter()
        self.gate_directions = build_231_gate_directions()

        self.char_encoder = nn.Embedding(22, dim)

        self.layers = nn.ModuleList(
            [TorsionLayer(index=i, dim=dim) for i in range(1, 11)]
        )

        self.fractal_graph = DistributedFractalGraphLayer(dim=dim)
        self.torsional_projection = TorsionalProjection()

        self.logic_head = nn.Linear(dim, LOGIC_GATES)
        self.reconstruction_head = nn.Linear(dim, dim)

        self.drift_thresholds = nn.Parameter(
            torch.tensor([0.02, 0.02, 0.03, 0.03, 0.04, 0.01]),
            requires_grad=False,
        )

    def encode_letters(self, letter_indices: Sequence[int]) -> torch.Tensor:
        ids = torch.tensor(tuple(letter_indices), dtype=torch.long)
        if ids.ndim != 1 or ids.numel() != 3:
            raise ValueError("The current exact route contract expects 3 letters.")
        return self.char_encoder(ids).mean(dim=0, keepdim=True)

    def gate_direction_tensor(self, gate_id: int) -> torch.Tensor:
        if not 1 <= gate_id <= OUTER_GATE_COUNT:
            raise ValueError("gate_id must be in 1..231")
        return torch.tensor(
            self.gate_directions[gate_id - 1].vector_5d,
            dtype=self.char_encoder.weight.dtype,
            device=self.char_encoder.weight.device,
        )

    def forward(
        self,
        config: DynamicNameConfiguration,
    ) -> Dict[str, object]:
        route = self.router.route(config)

        state = self.encode_letters(config.letter_combination)
        layer_states: List[torch.Tensor] = []
        torsions: List[torch.Tensor] = []

        graph_energy = torch.zeros((), device=state.device, dtype=state.dtype)

        for layer_index, layer in enumerate(self.layers, start=1):
            state, torsion = layer(state)
            layer_states.append(state)
            torsions.append(torsion)

            if layer_index == 6:
                # Expand a compact state into a reusable graph configuration.
                # The graph has no new learned neuron identities.
                graph_nodes = state.repeat(
                    min(13, CONCEPT_SLOTS),
                    1,
                )
                graph_nodes, graph_energy = self.fractal_graph(
                    graph_nodes,
                    depths=2,
                )
                state = graph_nodes.mean(dim=0, keepdim=True)

        torsion_matrix = torch.cat(torsions, dim=0)
        torsion_6d = torsion_matrix.mean(dim=0, keepdim=True)

        correction_5d = self.torsional_projection(torsion_6d)
        gate_direction = self.gate_direction_tensor(route.gate_id).unsqueeze(0)

        # Couple the control projection with the deterministic gate direction.
        state = state + correction_5d.mean(dim=-1, keepdim=True) * state
        gate_embedding = gate_direction.mean(dim=-1, keepdim=True)
        state = state + gate_embedding * state

        logic_logits = self.logic_head(state).squeeze(0)
        reconstruction = self.reconstruction_head(state)

        cycle_error = torch.mean(
            (state - layer_states[0]) ** 2
        )

        return {
            "route": route,
            "state_5d_control": correction_5d,
            "gate_direction_5d": gate_direction,
            "torsion_6d": torsion_6d,
            "logic_logits": logic_logits,
            "reconstruction": reconstruction,
            "graph_energy": graph_energy,
            "cycle_error": cycle_error,
            "selected_logic_gate": int(torch.argmax(logic_logits).item()) + 1,
        }

    def meta_loss(
        self,
        config: DynamicNameConfiguration,
        model_output: Mapping[str, object],
        target_state: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        loss_fn = MetaLogicalLoss()

        route = model_output["route"]
        if not hasattr(route, "gate_id"):
            raise TypeError("model_output['route'] must be a ReversibleRoute")

        return loss_fn(
            source=target_state,
            reconstruction=model_output["reconstruction"],
            logic_logits=model_output["logic_logits"],
            target_gate=route.gate_id % LOGIC_GATES + 1,
            torsion_6d=model_output["torsion_6d"],
            drift_thresholds=self.drift_thresholds,
            topology_error=model_output["graph_energy"],
            cycle_error=model_output["cycle_error"],
        )

    def export_architecture(self) -> Dict[str, object]:
        return {
            "name": "Holistic5D6DNetwork",
            "dimensions": {
                "logic": 5,
                "drift": 6,
                "logical_concept_slots": 175,
                "logic_gates": 14,
                "outer_letter_gates": 231,
                "space_group_slots": 230,
            },
            "nested_layers": [
                "BASE_TERM_CAPSULE",
                "CONDITIONAL_IF_THEN",
                "SYLLOGISM_ROUTER",
                "MODULAR_LOOP_RESONATOR",
                "SPACE_GROUP_OPERATOR_SLOT",
                "DISTRIBUTED_FRACTAL_GRAPH",
                "INVERTIBLE_FLOW",
                "TORSION_COMPENSATOR",
                "CONTRADICTION_RESOLVER",
                "OMEGA_ORCHESTRATOR",
            ],
            "invariants": {
                "exact_three_letter_route": True,
                "new_neuron_allocation_for_sentence": False,
                "source_backed_space_group_operator_required": True,
            },
        }


__all__ = [
    "GateDirection",
    "Holistic5D6DNetwork",
    "MetaLogicalLoss",
    "TorsionLayer",
    "TorsionalProjection",
    "DistributedFractalGraphLayer",
    "build_231_gate_directions",
]
