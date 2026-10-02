from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Sequence, Tuple

from .space_group_layer import GateSpaceGroupRegistry
from .tinkin52 import Tinkin52
from .tziruf_manifold import (
    DynamicNameConfiguration,
    MaimonidesCombinatorialCrystalNetwork,
)


@dataclass
class UnifiedTinkinRuntime:
    """WANGA-facing composition of Tziruf, outer gate registry, and Tinkin-52."""

    machine: Tinkin52
    outer_registry: GateSpaceGroupRegistry
    combinatorial: MaimonidesCombinatorialCrystalNetwork

    @classmethod
    def create(cls) -> "UnifiedTinkinRuntime":
        return cls(
            machine=Tinkin52(),
            outer_registry=GateSpaceGroupRegistry(),
            combinatorial=MaimonidesCombinatorialCrystalNetwork(),
        )

    def route_dynamic_name(
        self,
        config: DynamicNameConfiguration,
    ) -> Dict[str, Any]:
        routing = self.combinatorial.process_dynamic_name(config)

        return {
            "name_id": config.name_id,
            "letter_combination": list(config.letter_combination),
            "assigned_space_group": config.assigned_space_group,
            "logic_gate_distribution": (
                routing["gate_probabilities"].tolist()
            ),
            "selected_logic_gate": routing["routing_gate"],
            "outer_gate_slots": 231,
            "space_group_slots": 230,
            "outer_mapping_state": "PENDING_SOURCE_MAPPING",
            "verification_state": "NOT_YET_VERIFIED",
        }

    def execute(
        self,
        config: DynamicNameConfiguration,
        signals: Sequence[Tuple[str, str]] | None = None,
    ) -> Dict[str, Any]:
        route = self.route_dynamic_name(config)

        # The outer manifold routes metadata; actual execution signals remain
        # explicit. This prevents an unverified 231→230 mapping from silently
        # becoming a physical/logical transformation.
        observation = self.machine.step(signals or self.machine.canonical_signals[:2])

        return {
            "routing": route,
            "observation": self.machine.export(observation),
        }

    def validate(self) -> Dict[str, Any]:
        machine_validation = self.machine.validate()
        outer_validation = self.outer_registry.validate()
        return {
            "tinkin": machine_validation,
            "outer": outer_validation,
            "concept_slots": 175,
            "logic_count_audit": {
                "declared": 175,
                "computed_from_gate_counts": 188,
                "delta": 13,
            },
        }


__all__ = ["UnifiedTinkinRuntime"]
