from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RouteDecision:
    target: str
    matched_rule: str
    priority: int


_RULES = (
    (100, "compute/runtime", "compute-infrastructure"),
    (90, "drift/evidence", "ai-drift-forensics"),
    (80, "vitruvius", "architecture-intelligence-vitruvius"),
    (10, "model", "model-fabric"),
)


def route_request(target: str, rules: Iterable[tuple[int, str, str]] = _RULES) -> RouteDecision:
    normalized = target.casefold()
    matches = [(priority, needle, destination) for priority, needle, destination in rules if needle.casefold() in normalized]
    if not matches:
        return RouteDecision("unrouted", "", 0)
    priority, needle, destination = max(matches, key=lambda item: (item[0], item[1]))
    return RouteDecision(destination, needle, priority)
