"""Deterministic execution-boundary graph.

The routing policy is framework-neutral so the repository can later expose the
same contract through LangGraph without making the framework itself the source
of truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class Route(str, Enum):
    AUDIT = "AUDIT"
    EXECUTE = "EXECUTE"
    QUARANTINE = "QUARANTINE"


@dataclass(frozen=True)
class GateState:
    provenance_ok: bool
    validation_ok: bool
    activation_requested: bool
    conflict_detected: bool = False


def route(state: GateState) -> Route:
    if state.conflict_detected:
        return Route.QUARANTINE
    if not state.provenance_ok or not state.validation_ok:
        return Route.AUDIT
    if state.activation_requested:
        return Route.EXECUTE
    return Route.AUDIT


def explain(state: GateState) -> Mapping[str, str]:
    destination = route(state)
    return {
        "destination": destination.value,
        "execution_allowed": str(destination is Route.EXECUTE).lower(),
        "reason": (
            "all admission gates passed"
            if destination is Route.EXECUTE
            else "execution boundary not satisfied"
        ),
    }
