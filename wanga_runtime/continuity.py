"""Deterministic session continuity and logical-consistency gate.

This module records minimal sufficient state for the next session. It does not claim
that a checkpoint is authoritative over newer repository/evidence state.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any


HALT = "STATUS: LOGICAL_HALT_TRIGGERED"
FIRST_ORDER_PARTS = ("internal", "external", "coordination")
SECOND_ORDER_PARTS = ("part_1", "part_2", "part_3")
PRIVATE_PARTS = ("part_1", "part_2", "part_3")


@dataclass(frozen=True)
class ConsistencyResult:
    valid: bool
    contradictions: tuple[str, ...] = ()
    missing_context: tuple[str, ...] = ()
    private_complete: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["contradictions"] = list(self.contradictions)
        data["missing_context"] = list(self.missing_context)
        return data


class LogicalConsistencyGate:
    """Checks structure across first-order, second-order, and private logic.

    The private layer is a completion layer for the particular investigation, not a
    third/higher logical order.
    """

    @staticmethod
    def _parts(value: Any, expected: tuple[str, ...], prefix: str,
               missing: list[str]) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            missing.append(prefix)
            return None
        result: dict[str, Any] = {}
        for part in expected:
            if part not in value:
                missing.append(f"{prefix}.{part}")
            else:
                result[part] = value[part]
        return result

    @classmethod
    def validate(cls, logic: Any) -> ConsistencyResult:
        missing: list[str] = []
        contradictions: list[str] = []

        if not isinstance(logic, dict):
            return ConsistencyResult(
                False, ("LOGIC_CONTEXT_MUST_BE_OBJECT",), tuple(missing)
            )

        first = cls._parts(logic.get("first_order"), FIRST_ORDER_PARTS,
                           "first_order", missing)
        second = cls._parts(logic.get("second_order"), SECOND_ORDER_PARTS,
                            "second_order", missing)
        private = cls._parts(logic.get("private_logic"), PRIVATE_PARTS,
                             "private_logic", missing)

        # Explicit cross-level declarations prevent accidental promotion of the
        # private layer into another logical order.
        if logic.get("private_is_higher_order") is True:
            contradictions.append("PRIVATE_LOGIC_IS_NOT_A_HIGHER_ORDER")

        if logic.get("private_complete") is True:
            if private is None or any(v in (None, "") for v in private.values()):
                contradictions.append("PRIVATE_LOGIC_MARKED_COMPLETE_WITH_MISSING_PART")
        private_complete = logic.get("private_complete") is True and not any(
            item.startswith("private_logic.") for item in missing
        )

        if logic.get("investigation_complete") is True and not private_complete:
            contradictions.append("INVESTIGATION_CLOSED_BEFORE_PRIVATE_COMPLETION")

        # A caller may explicitly report a cross-level conflict. It must not be
        # silently normalized away.
        for conflict in logic.get("contradictions", []) or []:
            if conflict not in contradictions:
                contradictions.append(str(conflict))

        valid = not missing and not contradictions
        return ConsistencyResult(
            valid, tuple(contradictions), tuple(missing), private_complete
        )


@dataclass(frozen=True)
class SessionCheckpoint:
    checkpoint_id: str
    central_objective: str
    current_status: str
    last_completed_action: str
    facts: tuple[str, ...]
    decisions: tuple[str, ...]
    evidence: tuple[dict[str, Any], ...]
    repository: dict[str, Any]
    files_changed: tuple[str, ...]
    blockers: tuple[str, ...]
    open_questions: tuple[str, ...]
    remaining_gap: tuple[str, ...]
    next_action: dict[str, Any]
    do_not_do: tuple[str, ...]
    unverified_claims: tuple[str, ...]
    logical_consistency: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in (
            "facts", "decisions", "files_changed", "blockers",
            "open_questions", "remaining_gap", "do_not_do", "unverified_claims"
        ):
            data[key] = list(data[key])
        data["evidence"] = list(data["evidence"])
        return data

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )


def checkpoint_digest(checkpoint: SessionCheckpoint) -> str:
    return sha256(checkpoint.to_json().encode("utf-8")).hexdigest()


def build_checkpoint(**kwargs: Any) -> SessionCheckpoint:
    required = (
        "checkpoint_id", "central_objective", "current_status",
        "last_completed_action", "next_action", "logical_consistency"
    )
    missing = [key for key in required if key not in kwargs]
    if missing:
        raise ValueError(f"missing checkpoint fields: {','.join(missing)}")

    if not isinstance(kwargs["next_action"], dict) or not kwargs["next_action"].get("id"):
        raise ValueError("next_action must contain an id")

    return SessionCheckpoint(
        checkpoint_id=str(kwargs["checkpoint_id"]),
        central_objective=str(kwargs["central_objective"]),
        current_status=str(kwargs["current_status"]),
        last_completed_action=str(kwargs["last_completed_action"]),
        facts=tuple(kwargs.get("facts", ())),
        decisions=tuple(kwargs.get("decisions", ())),
        evidence=tuple(kwargs.get("evidence", ())),
        repository=dict(kwargs.get("repository", {})),
        files_changed=tuple(kwargs.get("files_changed", ())),
        blockers=tuple(kwargs.get("blockers", ())),
        open_questions=tuple(kwargs.get("open_questions", ())),
        remaining_gap=tuple(kwargs.get("remaining_gap", ())),
        next_action=dict(kwargs["next_action"]),
        do_not_do=tuple(kwargs.get("do_not_do", ())),
        unverified_claims=tuple(kwargs.get("unverified_claims", ())),
        logical_consistency=dict(kwargs["logical_consistency"]),
    )


def validate_checkpoint(checkpoint: SessionCheckpoint) -> tuple[str, ...]:
    errors: list[str] = []
    if not checkpoint.central_objective:
        errors.append("MISSING_CENTRAL_OBJECTIVE")
    if not checkpoint.current_status:
        errors.append("MISSING_CURRENT_STATUS")
    if not checkpoint.next_action.get("id"):
        errors.append("MISSING_NEXT_ACTION_ID")
    if not checkpoint.next_action.get("description"):
        errors.append("MISSING_NEXT_ACTION_DESCRIPTION")
    return tuple(errors)
