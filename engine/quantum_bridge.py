"""Deterministic mathematical bridge used by the VQB Cubity simulator.

Implements vector fusion, fixed-point iteration, and a dimensionless 5D
ring embedding. This is a software model, not a physical quantum or
relativistic implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, isfinite, sin
from typing import Sequence

Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]


@dataclass(frozen=True, slots=True)
class LanguagePoint:
    """A same-dimension fusion of wave, particle, and time feature vectors."""
    vector: Vector

    def __post_init__(self) -> None:
        if not self.vector:
            raise ValueError("LanguagePoint vector must not be empty")
        if not all(isfinite(v) for v in self.vector):
            raise ValueError("LanguagePoint vector must contain only finite values")


@dataclass(frozen=True, slots=True)
class FixedPointMergeResult:
    """Result and diagnostics for the requested fixed-point recurrence."""
    point: LanguagePoint
    initial_point: LanguagePoint
    iterations: int
    converged: bool
    residual: float


@dataclass(frozen=True, slots=True)
class RingPoint5D:
    """Dimensionless 5D coordinate on a configured ring-like embedding."""
    coordinates: tuple[float, float, float, float, float]

    def as_dict(self) -> dict[str, float]:
        return {f"x{i}": value for i, value in enumerate(self.coordinates, start=1)}


def _coerce_vector(values: Sequence[float], label: str) -> Vector:
    if not values:
        raise ValueError(f"{label} vector must not be empty")
    try:
        result = tuple(float(value) for value in values)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} vector must contain numeric values") from exc
    if not all(isfinite(value) for value in result):
        raise ValueError(f"{label} vector must contain only finite values")
    return result


def unified_language_point(
    wave_vector: Sequence[float],
    particle_vector: Sequence[float],
    time_vector: Sequence[float],
) -> LanguagePoint:
    """Fuse three equal-dimensional vectors by an explicit unweighted mean.

    This is a neutral fusion convention, not a learned weight scheme and not
    a claim that a physical wave-particle equation has been established.
    """
    wave = _coerce_vector(wave_vector, "wave")
    particle = _coerce_vector(particle_vector, "particle")
    time = _coerce_vector(time_vector, "time")
    if not (len(wave) == len(particle) == len(time)):
        raise ValueError("wave, particle, and time vectors must have the same dimension")
    return LanguagePoint(tuple((w + p + t) / 3.0 for w, p, t in zip(wave, particle, time)))


def _sign(value: float) -> float:
    if value > 0:
        return 1.0
    if value < 0:
        return -1.0
    return 0.0


def _validate_weight_matrix(matrix: Sequence[Sequence[float]], dimension: int) -> Matrix:
    if len(matrix) != dimension or any(len(row) != dimension for row in matrix):
        raise ValueError("W must be a square matrix matching the language-point dimension")
    converted = tuple(tuple(float(v) for v in row) for row in matrix)
    if not all(isfinite(v) for row in converted for v in row):
        raise ValueError("W must contain only finite values")
    return converted


def merge_three_language_points(
    points: Sequence[LanguagePoint],
    *,
    gamma: float = 0.5,
    weight_matrix: Sequence[Sequence[float]] | None = None,
    max_iterations: int = 512,
    tolerance: float = 1e-10,
) -> FixedPointMergeResult:
    """Merge three points using x[t+1] = gamma*x[t] + (1-gamma)*W*sign(x[t]).

    If W is omitted, the identity matrix is used as a neutral operator. This
    is a simulation default, not an inferred or learned weight set. Failure
    to converge is reported explicitly.
    """
    if len(points) != 3:
        raise ValueError("exactly three LanguagePoint values are required")
    dimension = len(points[0].vector)
    if any(len(point.vector) != dimension for point in points):
        raise ValueError("all LanguagePoint vectors must have the same dimension")
    if not isfinite(gamma) or not 0.0 <= gamma < 1.0:
        raise ValueError("gamma must be finite and satisfy 0 <= gamma < 1")
    if max_iterations < 1:
        raise ValueError("max_iterations must be >= 1")
    if not isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and > 0")

    if weight_matrix is None:
        weights: Matrix = tuple(
            tuple(1.0 if row == col else 0.0 for col in range(dimension))
            for row in range(dimension)
        )
    else:
        weights = _validate_weight_matrix(weight_matrix, dimension)

    initial = tuple(sum(point.vector[index] for point in points) / 3.0 for index in range(dimension))
    current = initial
    residual = float("inf")
    for iteration in range(1, max_iterations + 1):
        signed = tuple(_sign(value) for value in current)
        weighted = tuple(
            sum(weights[row][col] * signed[col] for col in range(dimension))
            for row in range(dimension)
        )
        updated = tuple(
            gamma * current[index] + (1.0 - gamma) * weighted[index]
            for index in range(dimension)
        )
        residual = max(abs(updated[index] - current[index]) for index in range(dimension))
        current = updated
        if residual <= tolerance:
            return FixedPointMergeResult(
                point=LanguagePoint(current),
                initial_point=LanguagePoint(initial),
                iterations=iteration,
                converged=True,
                residual=residual,
            )

    return FixedPointMergeResult(
        point=LanguagePoint(current),
        initial_point=LanguagePoint(initial),
        iterations=max_iterations,
        converged=False,
        residual=residual,
    )


def map_to_5d_ring(
    point: LanguagePoint,
    *,
    major_radius: float = 1.0,
    minor_radius: float = 0.25,
) -> RingPoint5D:
    """Map five vector channels to a dimensionless 5D ring-like coordinate.

    The radii are visualization parameters, not physical constants or a
    solution to Einstein's field equations.
    """
    if len(point.vector) < 5:
        raise ValueError("5D ring mapping requires a LanguagePoint with at least 5 dimensions")
    if not isfinite(major_radius) or major_radius <= 0.0:
        raise ValueError("major_radius must be finite and > 0")
    if not isfinite(minor_radius) or minor_radius < 0.0:
        raise ValueError("minor_radius must be finite and >= 0")
    x1, x2, x3, x4, x5 = point.vector[:5]
    theta = atan2(x2, x1)
    phi = atan2(x5, x4)
    coords = (
        (major_radius + minor_radius * cos(phi)) * cos(theta),
        (major_radius + minor_radius * cos(phi)) * sin(theta),
        minor_radius * sin(phi) + x3,
        minor_radius * cos(phi),
        minor_radius * sin(phi),
    )
    return RingPoint5D(tuple(float(value) for value in coords))
