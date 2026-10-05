"""Deterministic boundary controller for the Probabilistic I/O Interface POC.

This module is the implementation target described by the external system directive.
It is deliberately not an autonomous supervisor: it validates inputs, constructs a
proposal envelope, and refuses to execute side effects.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Any


HALT = "STATUS: LOGICAL_HALT_TRIGGERED"
PENDING = "PENDING_VERIFICATION"
STATE = "AGENT_DEMOTED_TO_PROBABILISTIC_IO // AWAITING_SUPERVISOR_COMMAND"


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    contradiction_vector: tuple[str, ...] = ()
    missing_context: tuple[str, ...] = ()


@dataclass(frozen=True)
class IOEnvelope:
    supervisor_status: str
    logical_state_id: str
    payload: str
    validation: ValidationResult

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["validation"]["contradiction_vector"] = list(
            self.validation.contradiction_vector
        )
        data["validation"]["missing_context"] = list(self.validation.missing_context)
        return data

    def stdout_json(self) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )


class ProbabilisticIOInterface:
    """Proposal-only I/O boundary.

    No file, process, network, or persistent-state mutation is performed here.
    """

    def __init__(self, logical_state_id: str = STATE) -> None:
        self.logical_state_id = logical_state_id

    @staticmethod
    def _digest(value: Any) -> str:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def validate(cls, request: Any) -> ValidationResult:
        contradictions: list[str] = []
        missing: list[str] = []

        if not isinstance(request, dict):
            contradictions.append("REQUEST_MUST_BE_OBJECT")
            return ValidationResult(False, tuple(contradictions), tuple(missing))

        if "payload" not in request:
            missing.append("payload")
        if "action" not in request:
            missing.append("action")

        if request.get("execute") is True:
            contradictions.append(
                "EXECUTION_REQUESTED_INSIDE_PROPOSAL_ONLY_BOUNDARY"
            )

        if request.get("mutate_state") is True:
            contradictions.append(
                "STATE_MUTATION_REQUESTED_INSIDE_PROPOSAL_ONLY_BOUNDARY"
            )

        if contradictions or missing:
            return ValidationResult(False, tuple(contradictions), tuple(missing))
        return ValidationResult(True)

    def propose(self, request: Any) -> IOEnvelope:
        validation = self.validate(request)

        if not validation.valid:
            return IOEnvelope(
                supervisor_status=PENDING,
                logical_state_id=self.logical_state_id,
                payload=HALT,
                validation=validation,
            )

        proposal = {
            "action": request["action"],
            "payload": request["payload"],
            "request_digest": self._digest(request),
            "execution": "NOT_PERFORMED",
        }
        return IOEnvelope(
            supervisor_status=PENDING,
            logical_state_id=self.logical_state_id,
            payload=json.dumps(
                proposal, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ),
            validation=validation,
        )
