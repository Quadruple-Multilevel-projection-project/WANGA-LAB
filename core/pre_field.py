"""Pre-Field admission boundary.

This module deliberately implements a conservative, testable boundary:
unresolved input remains UNCLASSIFIED until the caller supplies an explicit
field definition. It does not claim that removing numbers, time, or space
from arbitrary text is scientifically valid; those concepts are represented
as explicit admission constraints instead.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class AdmissionState(str, Enum):
    UNDIFFERENTIATED = "UNDIFFERENTIATED"
    INITIALIZED = "INITIALIZED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class FieldDefinition:
    name: str
    dimensions: tuple[str, ...] = ()
    allow_numeric: bool = True
    allow_temporal: bool = True
    allow_spatial: bool = True


@dataclass
class PreFieldState:
    state: AdmissionState = AdmissionState.UNDIFFERENTIATED
    observations: list[Mapping[str, Any]] = field(default_factory=list)
    rejection_reasons: list[str] = field(default_factory=list)


class PreField:
    """Explicit admission gate for evidence-bearing observations."""

    def __init__(self) -> None:
        self.state = PreFieldState()

    def initialize(self, definition: FieldDefinition) -> None:
        if not definition.name.strip():
            raise ValueError("field name must not be empty")
        self.state.state = AdmissionState.INITIALIZED
        self.state.rejection_reasons.clear()

    def admit(self, observation: Mapping[str, Any], definition: FieldDefinition) -> bool:
        if self.state.state != AdmissionState.INITIALIZED:
            raise RuntimeError("PreField must be initialized before admission")

        reasons: list[str] = []
        if not definition.allow_numeric and any(
            isinstance(v, (int, float)) and not isinstance(v, bool)
            for v in observation.values()
        ):
            reasons.append("NUMERIC_INPUT_NOT_PERMITTED")
        if not definition.allow_temporal and any(
            k.lower() in {"time", "timestamp", "date", "datetime"}
            for k in observation
        ):
            reasons.append("TEMPORAL_INPUT_NOT_PERMITTED")
        if not definition.allow_spatial and any(
            k.lower() in {"x", "y", "z", "lat", "lon", "longitude", "latitude", "location"}
            for k in observation
        ):
            reasons.append("SPATIAL_INPUT_NOT_PERMITTED")

        if reasons:
            self.state.rejection_reasons.extend(reasons)
            self.state.state = AdmissionState.REJECTED
            return False

        self.state.observations.append(dict(observation))
        return True
