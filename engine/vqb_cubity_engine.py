"""Deterministic VQB Cubity route simulator over 36 named sub-spaces.

The graph, language vectors, fixed-point merge, ring coordinates, and command
records are software abstractions. "TUNNELED" and "time_jump" are simulated
labels; they do not assert real quantum tunnelling or time travel.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import cos, sin
from typing import Any

from engine.quantum_bridge import (
    FixedPointMergeResult,
    LanguagePoint,
    map_to_5d_ring,
    merge_three_language_points,
    unified_language_point,
)

SUB_SPACE_COUNT = 36
MULTISCALE_OFFSETS = (1, 2, 4, 8, 16)
DEFAULT_COMMAND = "MAJORANA_2"
DEFAULT_MODE = "MAJORANA_2_ENTANGLE"


@dataclass(frozen=True, slots=True)
class EulerianSubSpace:
    sub_space_id: int
    internal_node_id: str
    external_node_id: str
    neighbor_ids: tuple[int, ...]
    scale_offsets: tuple[int, ...] = MULTISCALE_OFFSETS
    self_similar_template_ref: str = "VQB_36_TEMPLATE"


@dataclass(frozen=True, slots=True)
class VQBCommand:
    step: int
    sub_space_id: int
    state: str
    command: str
    mode: str
    amplitude: float
    time_jump: bool
    visibility: tuple[str, str]
    composite_point_id: int
    ring_5d: tuple[float, float, float, float, float]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["visibility"] = list(self.visibility)
        data["ring_5d"] = list(self.ring_5d)
        return data


@dataclass(frozen=True, slots=True)
class SimulationReport:
    status: str
    steps_requested: int
    sub_spaces_configured: int
    unique_sub_spaces_visited: int
    language_points_merged: int
    composite_points_merged: int
    commands_generated: int
    commands: tuple[VQBCommand, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "steps_requested": self.steps_requested,
            "sub_spaces_configured": self.sub_spaces_configured,
            "unique_sub_spaces_visited": self.unique_sub_spaces_visited,
            "language_points_merged": self.language_points_merged,
            "composite_points_merged": self.composite_points_merged,
            "commands_generated": self.commands_generated,
            "commands": [command.to_dict() for command in self.commands],
        }


def build_eulerian_sub_spaces(count: int = SUB_SPACE_COUNT) -> tuple[EulerianSubSpace, ...]:
    """Build a 36-node cyclic multi-scale graph with inner/outer node IDs."""
    if count != SUB_SPACE_COUNT:
        raise ValueError(f"this configuration requires exactly {SUB_SPACE_COUNT} sub-spaces")
    neighbors: list[set[int]] = [set() for _ in range(count)]
    for source in range(count):
        for offset in MULTISCALE_OFFSETS:
            target = (source + offset) % count
            if target != source:
                neighbors[source].add(target + 1)
                neighbors[target].add(source + 1)
    return tuple(
        EulerianSubSpace(
            sub_space_id=index + 1,
            internal_node_id=f"INNER_{index + 1:02d}",
            external_node_id=f"OUTER_{index + 1:02d}",
            neighbor_ids=tuple(sorted(neighbors[index])),
        )
        for index in range(count)
    )


def _fractal_walk(steps: int) -> tuple[int, ...]:
    """Use repeating multiscale strides 1,2,4,8,16 around a 36-node cycle."""
    if steps < 1:
        raise ValueError("steps must be >= 1")
    current = 0
    route = [current + 1]
    for transition in range(steps - 1):
        current = (current + MULTISCALE_OFFSETS[transition % len(MULTISCALE_OFFSETS)]) % SUB_SPACE_COUNT
        route.append(current + 1)
    return tuple(route)


def _deterministic_vectors(step: int, sub_space_id: int, dimension: int = 5) -> tuple[tuple[float, ...], ...]:
    """Generate reproducible toy features; no random or external inputs are used."""
    wave = tuple(sin((step + 1) * (axis + 1) * 0.13) for axis in range(dimension))
    particle = tuple(cos(sub_space_id * (axis + 1) * 0.07) for axis in range(dimension))
    time = tuple(sin((step + 1) * 0.011 + axis * 0.3) for axis in range(dimension))
    return wave, particle, time


class VQBCubityEngine:
    """Run the VQB concept as a deterministic, inspectable software simulation."""

    def __init__(self, *, gamma: float = 0.5, max_fixed_point_iterations: int = 512) -> None:
        self.sub_spaces = build_eulerian_sub_spaces()
        self.gamma = gamma
        self.max_fixed_point_iterations = max_fixed_point_iterations

    def simulate(self, steps: int = 120) -> SimulationReport:
        if steps < 1 or steps % 3 != 0:
            raise ValueError("steps must be a positive multiple of 3 so each composite merges exactly 3 points")

        route = _fractal_walk(steps)
        language_points: list[LanguagePoint] = []
        for step, sub_space_id in enumerate(route):
            wave, particle, time = _deterministic_vectors(step, sub_space_id)
            language_points.append(unified_language_point(wave, particle, time))

        composite_results: list[FixedPointMergeResult] = []
        for start in range(0, len(language_points), 3):
            result = merge_three_language_points(
                language_points[start:start + 3],
                gamma=self.gamma,
                max_iterations=self.max_fixed_point_iterations,
            )
            if not result.converged:
                raise RuntimeError(
                    f"fixed-point merge did not converge for composite point {len(composite_results) + 1}"
                )
            composite_results.append(result)

        commands: list[VQBCommand] = []
        for step, sub_space_id in enumerate(route):
            composite_index = step // 3
            result = composite_results[composite_index]
            ring = map_to_5d_ring(result.point)
            dimension_index = step % len(result.initial_point.vector)
            amplitude = min(1.0, abs(result.initial_point.vector[dimension_index]))
            commands.append(
                VQBCommand(
                    step=step + 1,
                    sub_space_id=sub_space_id,
                    state="TUNNELED",
                    command=DEFAULT_COMMAND,
                    mode=DEFAULT_MODE,
                    amplitude=round(amplitude, 6),
                    time_jump=True,
                    visibility=("ON", "OFF"),
                    composite_point_id=composite_index + 1,
                    ring_5d=tuple(round(value, 9) for value in ring.coordinates),
                )
            )

        unique_visited = len({command.sub_space_id for command in commands})
        return SimulationReport(
            status="SIMULATED_NOT_PHYSICAL_VERIFICATION",
            steps_requested=steps,
            sub_spaces_configured=len(self.sub_spaces),
            unique_sub_spaces_visited=unique_visited,
            language_points_merged=len(language_points),
            composite_points_merged=len(composite_results),
            commands_generated=len(commands),
            commands=tuple(commands),
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "sub_space_count": len(self.sub_spaces),
            "sub_spaces": [asdict(space) for space in self.sub_spaces],
            "multiscale_offsets": list(MULTISCALE_OFFSETS),
            "self_similarity": "each sub-space references VQB_36_TEMPLATE; recursive copies are represented symbolically rather than infinitely expanded",
            "active_space_semantics": "one visible sub-space per simulation step; each command records ON then OFF",
            "physics_status": "software abstraction only; no physical tunnelling or time-jump claim",
        }
