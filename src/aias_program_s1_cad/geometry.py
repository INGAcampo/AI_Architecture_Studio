"""Foundational CAD point, bounding-box and rotation geometry."""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, sin, radians, hypot

@dataclass(frozen=True, slots=True)
class Point:
    """Immutable planar CAD coordinate."""
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Execute the public Point.distance_to operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return hypot(other.x - self.x, other.y - self.y)

@dataclass(frozen=True, slots=True)
class BoundingBox:
    """Axis-aligned extent used for selection and spatial queries."""
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def contains_point(self, p: Point) -> bool:
        """Execute the public BoundingBox.contains_point operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return self.min_x <= p.x <= self.max_x and self.min_y <= p.y <= self.max_y

    def contains_box(self, other: "BoundingBox") -> bool:
        """Execute the public BoundingBox.contains_box operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return (
            self.min_x <= other.min_x and self.min_y <= other.min_y
            and self.max_x >= other.max_x and self.max_y >= other.max_y
        )

    def intersects(self, other: "BoundingBox") -> bool:
        """Execute the public BoundingBox.intersects operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return not (
            self.max_x < other.min_x or other.max_x < self.min_x
            or self.max_y < other.min_y or other.max_y < self.min_y
        )

def rotate_point(point: Point, base: Point, angle_degrees: float) -> Point:
    """Return a point rotated about a base by a counterclockwise degree angle."""
    angle = radians(angle_degrees)
    dx, dy = point.x - base.x, point.y - base.y
    return Point(
        base.x + dx * cos(angle) - dy * sin(angle),
        base.y + dx * sin(angle) + dy * cos(angle),
    )
