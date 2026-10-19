"""AI231 deterministic decision boundary.

This is an operational gate, not an interpretation of the canonical text.
known_source_refs must come from the locked sentence registry, not neural output.
Neural proposals are recorded as advisory input and never determine outcome.
"""
from dataclasses import dataclass
from typing import Collection, Literal, Optional

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
    known_source_refs: Collection[str],
    neural_proposal: Optional[str] = None,
) -> DecisionResult:
    """Return a result controlled only by the formal gate and locked source registry."""
    if not source_ref or source_ref not in known_source_refs:
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
