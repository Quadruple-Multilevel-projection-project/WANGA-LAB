"""Deterministic semantic routing to the six external-work spheres."""
from __future__ import annotations

SPHERES = (
    "Sphere_PHYSICAL", "Sphere_PLACE", "Sphere_THOUGHT",
    "Sphere_ADVICE", "Sphere_WILL", "Sphere_INTELLECT",
)

_RULES = (
    ("Sphere_PLACE", ("location", "place", "distance", "coordinate", "route", "triangulation")),
    ("Sphere_PHYSICAL", ("physical", "mass", "force", "material", "hardware")),
    ("Sphere_THOUGHT", ("analyze", "reason", "logic", "explain", "compare")),
    ("Sphere_ADVICE", ("recommend", "advice", "suggest", "should")),
    ("Sphere_WILL", ("plan", "intend", "goal", "choose", "decision")),
    ("Sphere_INTELLECT", ("calculate", "compute", "python", "function", "math")),
)

def route_request(text: str) -> str:
    """Return first matching sphere; unknown/ambiguous requests fail closed."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Empty request cannot be routed")
    lowered = text.casefold()
    matches = [sphere for sphere, terms in _RULES if any(term in lowered for term in terms)]
    if len(matches) != 1:
        raise ValueError(f"Routing is ambiguous or unsupported: {matches}")
    return matches[0]
