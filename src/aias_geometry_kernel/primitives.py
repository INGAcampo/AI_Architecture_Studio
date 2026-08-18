"""Immutable two-dimensional point, vector, line, circle and bounding-box primitives."""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True, slots=True)
class Point2D:
    """Cartesian point with finite x and y coordinates."""
    x: float
    y: float
    def distance_to(self, other: "Point2D") -> float:
        """Return Euclidean distance to another planar point."""
        return math.hypot(self.x-other.x, self.y-other.y)

@dataclass(frozen=True, slots=True)
class Vector2D:
    """Cartesian displacement supporting magnitude and normalized direction."""
    x: float
    y: float
    @property
    def magnitude(self) -> float:
        """Return vector length from its Cartesian components."""
        return math.hypot(self.x, self.y)
    def normalized(self) -> "Vector2D":
        """Return a unit vector and reject zero-length input."""
        m = self.magnitude
        if m == 0:
            raise ValueError("zero_vector")
        return Vector2D(self.x/m, self.y/m)
    def dot(self, other: "Vector2D") -> float:
        """Return the scalar dot product with another vector."""
        return self.x*other.x + self.y*other.y
    def cross(self, other: "Vector2D") -> float:
        """Return the signed scalar two-dimensional cross product."""
        return self.x*other.y - self.y*other.x

@dataclass(frozen=True, slots=True)
class Line2D:
    """Directed finite line segment defined by distinct start and end points."""
    start: Point2D
    end: Point2D
    @property
    def length(self) -> float:
        """Return segment length between start and end points."""
        return self.start.distance_to(self.end)
    @property
    def direction(self) -> Vector2D:
        """Return the normalized direction from start to end."""
        return Vector2D(self.end.x-self.start.x, self.end.y-self.start.y).normalized()

@dataclass(frozen=True, slots=True)
class Circle2D:
    """Circular curve defined by center and strictly positive radius."""
    center: Point2D
    radius: float
    def __post_init__(self):
        if self.radius <= 0:
            raise ValueError("radius_must_be_positive")
    @property
    def area(self) -> float:
        """Return circle area in squared coordinate units."""
        return math.pi*self.radius*self.radius
    @property
    def circumference(self) -> float:
        """Return circle perimeter in coordinate units."""
        return 2*math.pi*self.radius

@dataclass(frozen=True, slots=True)
class BoundingBox2D:
    """Axis-aligned spatial extent with ordered minimum and maximum coordinates."""
    min_point: Point2D
    max_point: Point2D
    def __post_init__(self):
        if self.min_point.x > self.max_point.x or self.min_point.y > self.max_point.y:
            raise ValueError("invalid_bounding_box")
    @property
    def width(self) -> float:
        """Return horizontal extent of the bounding box."""
        return self.max_point.x-self.min_point.x
    @property
    def height(self) -> float:
        """Return vertical extent of the bounding box."""
        return self.max_point.y-self.min_point.y
    def contains(self, p: Point2D) -> bool:
        """Test inclusive point containment within box limits."""
        return self.min_point.x <= p.x <= self.max_point.x and self.min_point.y <= p.y <= self.max_point.y
