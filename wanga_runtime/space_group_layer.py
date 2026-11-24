from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence, Tuple
import numpy as np

from .tinkin52 import HEBREW_LETTERS


@dataclass(frozen=True)
class SpaceGroupOperatorSpec:
    """Data contract for one crystallographic space-group operator.

    The operator payload is intentionally source-backed. A placeholder group
    has no rotation/translation semantics and cannot be applied.
    """

    group_number: int
    symbol: str | None = None
    crystal_system: str | None = None
    rotation: Tuple[Tuple[float, float, float], ...] | None = None
    translation: Tuple[float, float, float] | None = None
    source_status: str = "PENDING_SOURCE"
    source_ref: str | None = None

    @property
    def verified(self) -> bool:
        return (
            self.source_status == "VERIFIED"
            and self.rotation is not None
            and self.translation is not None
        )

    def apply(self, xyz: Sequence[float]) -> np.ndarray:
        if not self.verified:
            raise ValueError(
                f"Space-group {self.group_number} has no verified operator payload."
            )

        vector = np.asarray(xyz, dtype=float)
        if vector.shape != (3,):
            raise ValueError("xyz must have shape (3,).")

        rotation = np.asarray(self.rotation, dtype=float)
        translation = np.asarray(self.translation, dtype=float)
        return rotation @ vector + translation


@dataclass(frozen=True)
class GlobalGate:
    gate_index: int
    letter_a: str
    letter_b: str

    def __post_init__(self) -> None:
        if self.letter_a == self.letter_b:
            raise ValueError("A global gate must contain two distinct letters.")


def build_231_global_gates() -> Tuple[GlobalGate, ...]:
    gates = []
    index = 1

    for i, a in enumerate(HEBREW_LETTERS):
        for b in HEBREW_LETTERS[i + 1:]:
            gates.append(GlobalGate(index, a, b))
            index += 1

    if len(gates) != 231:
        raise RuntimeError(f"Expected 231 unique unordered gates, got {len(gates)}.")

    return tuple(gates)


class GateSpaceGroupRegistry:
    """Registry separating alphabetical gates from crystallographic operators."""

    def __init__(
        self,
        gates: Iterable[GlobalGate] | None = None,
        groups: Mapping[int, SpaceGroupOperatorSpec] | None = None,
    ) -> None:
        self.gates = tuple(gates or build_231_global_gates())
        self.groups: Dict[int, SpaceGroupOperatorSpec] = dict(groups or {})

        if len(self.gates) != 231:
            raise ValueError("Gate registry must contain exactly 231 gates.")

    def register_group(self, spec: SpaceGroupOperatorSpec) -> None:
        if not 1 <= spec.group_number <= 230:
            raise ValueError("Space-group number must be in 1..230.")
        self.groups[spec.group_number] = spec

    def get_group(self, group_number: int) -> SpaceGroupOperatorSpec:
        if not 1 <= group_number <= 230:
            raise KeyError(f"Unknown space-group slot: {group_number}")
        return self.groups.get(
            group_number,
            SpaceGroupOperatorSpec(group_number=group_number),
        )

    def gate(self, gate_index: int) -> GlobalGate:
        if not 1 <= gate_index <= 231:
            raise KeyError(f"Unknown gate index: {gate_index}")
        return self.gates[gate_index - 1]

    def assign_gate(
        self,
        gate_index: int,
        space_group_number: int,
        *,
        mapping_type: str = "SOURCE_PENDING",
    ) -> Dict[str, object]:
        if not 1 <= gate_index <= 231:
            raise ValueError("gate_index must be in 1..231")
        if not 1 <= space_group_number <= 230:
            raise ValueError("space_group_number must be in 1..230")

        return {
            "gate_index": gate_index,
            "gate_pair": (
                self.gate(gate_index).letter_a,
                self.gate(gate_index).letter_b,
            ),
            "space_group_number": space_group_number,
            "mapping_type": mapping_type,
        }

    def validate(self) -> Dict[str, object]:
        return {
            "global_gate_count": len(self.gates),
            "space_group_slots": 230,
            "loaded_space_group_payloads": sum(
                spec.verified for spec in self.groups.values()
            ),
            "pending_space_group_payloads":
                230 - sum(spec.verified for spec in self.groups.values()),
            "requires_source_mapping":
                len(self.gates) == 231,
        }


@dataclass(frozen=True)
class NestedConfiguration:
    """Compact configuration pointer; does not allocate new concept neurons."""

    nesting_level: int
    base_elements: Tuple[int, ...]
    space_group_id: int | None
    sub_configs: Tuple["NestedConfiguration", ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.nesting_level <= 4:
            raise ValueError("nesting_level must be in 0..4")
        if any(not 1 <= x <= 175 for x in self.base_elements):
            raise ValueError("base_elements must reference concept IDs 1..175")
        if self.space_group_id is not None and not 1 <= self.space_group_id <= 230:
            raise ValueError("space_group_id must be in 1..230")

    def as_dict(self) -> Dict[str, object]:
        return {
            "nesting_level": self.nesting_level,
            "base_elements": list(self.base_elements),
            "space_group_id": self.space_group_id,
            "sub_configs": [x.as_dict() for x in self.sub_configs],
        }


__all__ = [
    "GlobalGate",
    "GateSpaceGroupRegistry",
    "NestedConfiguration",
    "SpaceGroupOperatorSpec",
    "build_231_global_gates",
]
