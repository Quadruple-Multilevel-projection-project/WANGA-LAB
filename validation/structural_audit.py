"""Conservative structural audit primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from crypto.poc_generator import generate_cch


@dataclass(frozen=True)
class AuditResult:
    status: str
    cch: str
    reasons: tuple[str, ...] = ()


def audit_record(record: Mapping[str, Any]) -> AuditResult:
    reasons: list[str] = []
    required = ("id", "source", "validation_state")
    for key in required:
        if key not in record:
            reasons.append(f"MISSING_{key.upper()}")

    status = "STRUCTURALLY_VALID" if not reasons else "STRUCTURALLY_INVALID"
    return AuditResult(status=status, cch=generate_cch(record), reasons=tuple(reasons))
