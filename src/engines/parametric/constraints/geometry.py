from __future__ import annotations

from math import isclose

from .types import ConstraintPoint, ConstraintSegment


def dot(a: ConstraintSegment, b: ConstraintSegment) -> float:
    return a.dx * b.dx + a.dy * b.dy + a.dz * b.dz


def cross_z(a: ConstraintSegment, b: ConstraintSegment) -> float:
    return a.dx * b.dy - a.dy * b.dx


def points_close(a: ConstraintPoint, b: ConstraintPoint, tolerance: float = 1e-6) -> bool:
    return (
        isclose(a.x, b.x, abs_tol=tolerance)
        and isclose(a.y, b.y, abs_tol=tolerance)
        and isclose(a.z, b.z, abs_tol=tolerance)
    )


def horizontal(segment: ConstraintSegment, tolerance: float = 1e-6) -> bool:
    return abs(segment.dy) <= tolerance and abs(segment.dz) <= tolerance


def vertical(segment: ConstraintSegment, tolerance: float = 1e-6) -> bool:
    return abs(segment.dx) <= tolerance and abs(segment.dz) <= tolerance


def parallel(a: ConstraintSegment, b: ConstraintSegment, tolerance: float = 1e-6) -> bool:
    if a.length <= tolerance or b.length <= tolerance:
        return False
    return abs(cross_z(a, b)) <= tolerance * max(a.length, b.length, 1.0)


def perpendicular(a: ConstraintSegment, b: ConstraintSegment, tolerance: float = 1e-6) -> bool:
    if a.length <= tolerance or b.length <= tolerance:
        return False
    return abs(dot(a, b)) <= tolerance * max(a.length * b.length, 1.0)


def equal_length(a: ConstraintSegment, b: ConstraintSegment, tolerance: float = 1e-6) -> bool:
    return isclose(a.length, b.length, abs_tol=tolerance)


def point_distance(a: ConstraintPoint, b: ConstraintPoint) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5
