from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Dict, List, Mapping, Sequence, Tuple

import torch
import torch.nn.functional as F


LETTER_COUNT = 22
OUTER_GATE_COUNT = 231
SPACE_GROUP_COUNT = 230
LOGIC_GATE_COUNT = 14


def stable_seed(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode("utf-8")
    return int.from_bytes(sha256(payload).digest()[:8], "big") % (2**31 - 1)


@dataclass(frozen=True)
class DynamicNameConfiguration:
    """Runtime configuration produced by the combinatorial manifold.

    letter_combination contains alphabet indices in [0, 21].
    assigned_space_group is a slot in [1, 230]. The slot is metadata until a
    source-backed crystallographic operator is attached.
    """

    name_id: int
    letter_combination: Tuple[int, ...]
    assigned_space_group: int
    source_status: str = "GENERATED"
    source_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.letter_combination:
            raise ValueError("letter_combination cannot be empty")
        if any(not 0 <= i < LETTER_COUNT for i in self.letter_combination):
            raise ValueError("letter indices must be in 0..21")
        if not 1 <= self.assigned_space_group <= SPACE_GROUP_COUNT:
            raise ValueError("assigned_space_group must be in 1..230")


class SeferHaTzirufManifold:
    """Deterministic combination source.

    This class deliberately separates generation from interpretation. It can
    later be replaced by a source-backed Sefer ha-Tziruf corpus without
    changing the routing contract.
    """

    def __init__(self, vocab_size: int = LETTER_COUNT, combination_length: int = 3):
        self.vocab_size = vocab_size
        self.combination_length = combination_length

    def generate_name_weights(self, combination_id: int) -> Tuple[int, ...]:
        generator = torch.Generator(device="cpu")
        generator.manual_seed(stable_seed("tziruf", combination_id))
        indices = torch.randint(
            low=0,
            high=self.vocab_size,
            size=(self.combination_length,),
            generator=generator,
        )
        return tuple(int(x) for x in indices.tolist())

    def build_configuration(
        self,
        *,
        name_id: int,
        assigned_space_group: int,
        combination_id: int | None = None,
    ) -> DynamicNameConfiguration:
        cid = name_id if combination_id is None else combination_id
        return DynamicNameConfiguration(
            name_id=name_id,
            letter_combination=self.generate_name_weights(cid),
            assigned_space_group=assigned_space_group,
        )


class CombinatorialWeightOperator(torch.nn.Module):
    """Maps letter combinations to reusable vector weights.

    The operator is not a classical scalar W_ij. It produces a vector
    representation that can be used by downstream relational layers.
    """

    def __init__(self, embedding_dim: int = 16, seed: int = 52):
        super().__init__()

        generator = torch.Generator(device="cpu")
        generator.manual_seed(seed)

        weight = torch.empty(LETTER_COUNT, embedding_dim)
        torch.nn.init.xavier_uniform_(weight, generator=generator)
        self.letter_embeddings = torch.nn.Parameter(weight)

    def encode(self, letter_indices: torch.Tensor) -> torch.Tensor:
        if letter_indices.dtype != torch.long:
            raise TypeError("letter_indices must be torch.long")
        if letter_indices.ndim != 1:
            raise ValueError("letter_indices must have shape [sequence]")
        if torch.any(letter_indices < 0) or torch.any(letter_indices >= LETTER_COUNT):
            raise ValueError("letter_indices outside Hebrew alphabet range")

        embeddings = self.letter_embeddings(letter_indices)
        return embeddings.mean(dim=0)

    def pairwise_entanglement(
        self,
        letter_indices: torch.Tensor,
        node_coordinates: torch.Tensor,
        sigma: float = 1.0,
    ) -> torch.Tensor:
        """Semantic/geometry coupling score.

        E_ij = cos(e_i,e_j) * exp(-||p_i-p_j|| / sigma)

        The score is a computational coupling measure, not a physical
        quantum-entanglement claim.
        """

        embeddings = self.letter_embeddings(letter_indices)
        if embeddings.shape[0] < 2:
            return torch.zeros((), dtype=embeddings.dtype, device=embeddings.device)

        if node_coordinates.ndim != 2 or node_coordinates.shape[0] != embeddings.shape[0]:
            raise ValueError(
                "node_coordinates must have shape [len(letter_indices), 3]"
            )

        normalized = F.normalize(embeddings, dim=-1)
        cosine = normalized @ normalized.T

        distances = torch.cdist(node_coordinates, node_coordinates)
        geometry = torch.exp(-distances / max(sigma, 1e-6))

        mask = ~torch.eye(
            embeddings.shape[0],
            dtype=torch.bool,
            device=embeddings.device,
        )

        return (cosine * geometry)[mask].mean()


class DynamicRoutingEngine(torch.nn.Module):
    """Routes a dynamic name into the 14 logical gates."""

    def __init__(self, embedding_dim: int = 16, gate_count: int = LOGIC_GATE_COUNT):
        super().__init__()
        self.gate_projection = torch.nn.Linear(embedding_dim + 1, gate_count)

    def forward(
        self,
        combination_vector: torch.Tensor,
        assigned_space_group: int,
    ) -> torch.Tensor:
        if combination_vector.ndim != 1:
            raise ValueError("combination_vector must have shape [embedding_dim]")

        group_scalar = torch.tensor(
            [assigned_space_group / SPACE_GROUP_COUNT],
            dtype=combination_vector.dtype,
            device=combination_vector.device,
        )

        routing_input = torch.cat([combination_vector, group_scalar], dim=0)
        logits = self.gate_projection(routing_input)
        return torch.softmax(logits, dim=-1)


class MaimonidesCombinatorialCrystalNetwork(torch.nn.Module):
    """Three-tier runtime:
       Sefer ha-Tziruf → 231/230 outer manifold → 14-gate inner routing.
    """

    def __init__(self, embedding_dim: int = 16, seed: int = 52):
        super().__init__()
        self.sefer_tziruf = SeferHaTzirufManifold()
        self.weight_operator = CombinatorialWeightOperator(
            embedding_dim=embedding_dim,
            seed=seed,
        )
        self.routing = DynamicRoutingEngine(
            embedding_dim=embedding_dim,
            gate_count=LOGIC_GATE_COUNT,
        )

        # Outer gate slots and crystallographic slots are kept as separate
        # index spaces. A source-backed mapping may later populate this table.
        self.register_buffer(
            "outer_gate_slot_ids",
            torch.arange(1, OUTER_GATE_COUNT + 1, dtype=torch.long),
        )
        self.register_buffer(
            "space_group_slot_ids",
            torch.arange(1, SPACE_GROUP_COUNT + 1, dtype=torch.long),
        )

    def build_routing_vector(
        self,
        config: DynamicNameConfiguration,
    ) -> Dict[str, torch.Tensor]:
        letters = torch.tensor(config.letter_combination, dtype=torch.long)
        combination_vector = self.weight_operator.encode(letters)

        gate_probabilities = self.routing(
            combination_vector,
            config.assigned_space_group,
        )

        return {
            "combination_vector": combination_vector,
            "gate_probabilities": gate_probabilities,
        }

    def process_dynamic_name(
        self,
        config: DynamicNameConfiguration,
    ) -> Dict[str, object]:
        routed = self.build_routing_vector(config)

        return {
            "name_id": config.name_id,
            "letter_combination": list(config.letter_combination),
            "space_group_slot": config.assigned_space_group,
            "combination_vector": routed["combination_vector"].detach(),
            "gate_probabilities": routed["gate_probabilities"].detach(),
            "routing_gate": int(
                torch.argmax(routed["gate_probabilities"]).item()
            ) + 1,
            "outer_gate_slot_count": OUTER_GATE_COUNT,
            "space_group_slot_count": SPACE_GROUP_COUNT,
            "verification_state": "NOT_YET_VERIFIED",
        }


__all__ = [
    "CombinatorialWeightOperator",
    "DynamicNameConfiguration",
    "DynamicRoutingEngine",
    "MaimonidesCombinatorialCrystalNetwork",
    "SeferHaTzirufManifold",
]
