"""Fail-closed reference gate for WANGA / MAJORANA core operations.

This module is a policy evaluator, not an agent runtime or platform interceptor.
A caller must invoke it before dispatching a core operation and must refuse
dispatch unless the returned decision is PASS.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class GateDecision:
    status: str
    reasons: tuple[str, ...]
    receipt_sha256: str


def evaluate_task(envelope: Mapping[str, Any]) -> GateDecision:
    """Evaluate a task envelope. Missing evidence always blocks core work."""
    reasons: list[str] = []
    operation = envelope.get("requested_operation")

    if operation == "documentation_only":
        status = "PASS_FOR_REVIEW"
        reasons.append("Documentation-only recording; no core semantic execution authorized.")
    else:
        if envelope.get("constitutional_axiom_id") != "AXIOM-001":
            reasons.append("Missing or incorrect constitutional_axiom_id.")
        if not envelope.get("constitution_source_ref"):
            reasons.append("Canonical constitutional source reference is missing.")
        if not envelope.get("constitution_version"):
            reasons.append("Constitution version is missing.")
        if envelope.get("axiom_source_verified") is not True:
            reasons.append("Canonical axiom source has not been verified.")
        if not envelope.get("derived_law_refs"):
            reasons.append("No explicitly approved derived-law reference supplied.")
        if not operation or operation not in (envelope.get("allowed_operations") or []):
            reasons.append("Requested operation is not explicitly allowlisted.")
        if not envelope.get("source_refs"):
            reasons.append("Operation source evidence is missing.")
        if envelope.get("unresolved_conflicts"):
            reasons.append("Unresolved constitutional or semantic conflicts exist.")
        approval = envelope.get("architect_approval_receipt")
        if not isinstance(approval, str) or not approval.strip():
            reasons.append("Explicit architect approval receipt is missing.")
        status = "BLOCKED" if reasons else "PASS"

    receipt_body = {
        "status": status,
        "reasons": reasons,
        "task_id": envelope.get("task_id"),
        "message_id": envelope.get("message_id"),
        "requested_operation": operation,
        "constitutional_axiom_id": envelope.get("constitutional_axiom_id"),
        "constitution_version": envelope.get("constitution_version"),
    }
    digest = hashlib.sha256(
        json.dumps(receipt_body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return GateDecision(status=status, reasons=tuple(reasons), receipt_sha256=digest)


def may_dispatch(decision: GateDecision) -> bool:
    """Only PASS permits dispatch; PASS_FOR_REVIEW is not execution approval."""
    return decision.status == "PASS"
