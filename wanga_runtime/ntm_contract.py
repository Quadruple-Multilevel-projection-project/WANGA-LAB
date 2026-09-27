from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

SUPPORTED_NTM_MODES: Tuple[str, ...] = (
    "HIGH_LOGIC",
    "VERSION_DIFF",
    "SEMANTIC_DRIFT",
    "STRUCTURAL_DRIFT",
    "INTENT_RECOVERY",
    "FULL_NTM",
)


@dataclass(frozen=True)
class NTMContractAudit:
    schema_modes: Tuple[str, ...]
    runtime_modes: Tuple[str, ...]
    missing_runtime_modes: Tuple[str, ...]
    extra_runtime_modes: Tuple[str, ...]

    @property
    def status(self) -> str:
        return "PASS" if not self.missing_runtime_modes and not self.extra_runtime_modes else "FAIL"


def audit_ntm_contract(schema_modes: Tuple[str, ...] | list[str]) -> NTMContractAudit:
    schema = tuple(schema_modes)
    schema_set = set(schema)
    runtime_set = set(SUPPORTED_NTM_MODES)
    return NTMContractAudit(
        schema_modes=schema,
        runtime_modes=SUPPORTED_NTM_MODES,
        missing_runtime_modes=tuple(sorted(schema_set - runtime_set)),
        extra_runtime_modes=tuple(sorted(runtime_set - schema_set)),
    )
