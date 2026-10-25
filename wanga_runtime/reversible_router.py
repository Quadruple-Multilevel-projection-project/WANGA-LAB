from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence, Tuple

import torch

from .tziruf_manifold import DynamicNameConfiguration


LETTER_COUNT = 22
TRIPLE_SPACE_SIZE = LETTER_COUNT ** 3
OUTER_GATE_COUNT = 231
SPACE_GROUP_COUNT = 230


def encode_triple(indices: Sequence[int]) -> int:
    """Exact base-22 encoding for a 3-letter combination."""
    if len(indices) != 3:
        raise ValueError("This reversible router expects exactly 3 letters.")
    if any(not 0 <= int(x) < LETTER_COUNT for x in indices):
        raise ValueError("Letter indices must be in 0..21.")

    a, b, c = (int(x) for x in indices)
    return (a * LETTER_COUNT + b) * LETTER_COUNT + c


def decode_triple(code: int) -> Tuple[int, int, int]:
    """Exact inverse of encode_triple."""
    if not 0 <= code < TRIPLE_SPACE_SIZE:
        raise ValueError("Triple code outside 0..10647.")

    c = code % LETTER_COUNT
    q = code // LETTER_COUNT
    b = q % LETTER_COUNT
    a = q // LETTER_COUNT
    return a, b, c


def gate_index_from_code(code: int) -> int:
    """Deterministic outer routing slot in 1..231."""
    return (code % OUTER_GATE_COUNT) + 1


def residual_from_code(code: int) -> int:
    """Lossless quotient required to reconstruct the triple."""
    return code // OUTER_GATE_COUNT


def space_group_slot_from_code(code: int) -> int:
    """Deterministic routing slot in 1..230.

    This is a routing slot only. It is not asserted to be a crystallographic
    space-group assignment until a source-backed mapping is loaded.
    """
    return (code % SPACE_GROUP_COUNT) + 1


@dataclass(frozen=True)
class ReversibleRoute:
    combination_code: int
    gate_id: int
    residual: int
    space_group_slot: int

    def reconstruct(self) -> Tuple[int, int, int]:
        code = self.gate_id - 1 + OUTER_GATE_COUNT * self.residual
        return decode_triple(code)

    def as_dict(self) -> Dict[str, int]:
        return {
            "combination_code": self.combination_code,
            "gate_id": self.gate_id,
            "residual": self.residual,
            "space_group_slot": self.space_group_slot,
        }


class ReversibleCombinatorialRouter:
    """Exact 3-letter router over the 22^3 combination space.

    The route carries a compact discrete inverse key rather than relying on a
    lossy neural embedding. Embeddings may be added downstream for semantics,
    but reconstruction uses the integer route key.
    """

    def route(self, config: DynamicNameConfiguration) -> ReversibleRoute:
        route_code = encode_triple(config.letter_combination)
        return ReversibleRoute(
            combination_code=route_code,
            gate_id=gate_index_from_code(route_code),
            residual=residual_from_code(route_code),
            space_group_slot=space_group_slot_from_code(route_code),
        )

    def reconstruct(
        self,
        route: ReversibleRoute,
    ) -> DynamicNameConfiguration:
        indices = route.reconstruct()

        # Confirm route integrity before reconstruction.
        if encode_triple(indices) != route.combination_code:
            raise RuntimeError("Route integrity check failed.")

        return DynamicNameConfiguration(
            name_id=0,
            letter_combination=indices,
            assigned_space_group=route.space_group_slot,
            source_status="RECONSTRUCTED_FROM_ROUTE",
        )

    def address_5d(
        self,
        route: ReversibleRoute,
    ) -> torch.Tensor:
        """Stable numeric [X,Y,Z,T,N] routing address.

        This is an addressing coordinate, not a claim of physical position.
        """
        code = float(route.combination_code)
        return torch.tensor(
            [
                (route.gate_id - 1) / (OUTER_GATE_COUNT - 1),
                route.residual / 46.0,
                (route.space_group_slot - 1) / (SPACE_GROUP_COUNT - 1),
                code / (TRIPLE_SPACE_SIZE - 1),
                len(str(route.combination_code)) / 5.0,
            ],
            dtype=torch.float32,
        )


__all__ = [
    "ReversibleCombinatorialRouter",
    "ReversibleRoute",
    "decode_triple",
    "encode_triple",
    "gate_index_from_code",
    "residual_from_code",
    "space_group_slot_from_code",
]
