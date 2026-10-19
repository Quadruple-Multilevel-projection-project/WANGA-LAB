"""AI231 deterministic decision boundary.

This is an operational gate, not an interpretation of the canonical text.
The source-reference resolver must be backed by the locked sentence registry.
Neural proposals are recorded as advisory input and never determine outcome.
"""
from dataclasses import dataclass
from typing import Literal, Optional

FormalDecision = Literal["ACCEPT", "REJECT", "REQUIRES_REVIEW"]


@dataclass(frozen=True)
class DecisionResult:
    status: FormalDecision
    source_ref: Optional[str]
    reason: str
    neural_proposal: Optional[str] = None


def ai231_task(
    *,
    formal_decision: str,
    source_ref: Optional[str],
    source_ref_resolved: bool,
    neural_proposal: Optional[str] = None,
) -> DecisionResult:
    """Return a result controlled only by the formal gate and source evidence."""
    if not source_ref or not source_ref_resolved:
        return DecisionResult(
            status="REQUIRES_REVIEW",
            source_ref=source_ref,
            reason="SOURCE_REFERENCE_MISSING_OR_UNRESOLVED",
            neural_proposal=neural_proposal,
        )
    if formal_decision not in {"ACCEPT", "REJECT", "REQUIRES_REVIEW"}:
        return DecisionResult(
            status="REQUIRES_REVIEW",
            source_ref=source_ref,
            reason="UNKNOWN_FORMAL_DECISION",
            neural_proposal=neural_proposal,
        )
    return DecisionResult(
        status=formal_decision,  # type: ignore[arg-type]
        source_ref=source_ref,
        reason="FORMAL_GATE_RESULT",
        neural_proposal=neural_proposal,
    )
