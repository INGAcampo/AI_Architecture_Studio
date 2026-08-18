"""Distances, lengths, areas, angles and spatial extents for kernel geometry."""
from __future__ import annotations
import math
from .primitives import Point2D, Line2D, Vector2D

class MeasurementEngine:
    """Provide deterministic unit-agnostic measurements over validated primitives."""
    @staticmethod
    def angle_between(a: Vector2D, b: Vector2D) -> float:
        """Return the unsigned angle in radians between nonzero vectors."""
        denom = a.magnitude*b.magnitude
        if denom == 0:
            raise ValueError("zero_vector")
        value = max(-1.0,min(1.0,a.dot(b)/denom))
        return math.acos(value)

    @staticmethod
    def point_to_line_distance(point: Point2D, line: Line2D) -> float:
        """Compute shortest distance from a point to an infinite line."""
        dx = line.end.x-line.start.x
        dy = line.end.y-line.start.y
        if dx == 0 and dy == 0:
            return point.distance_to(line.start)
        return abs(dy*point.x-dx*point.y+line.end.x*line.start.y-line.end.y*line.start.x)/math.hypot(dx,dy)

    @staticmethod
    def project_point_on_line(point: Point2D, line: Line2D) -> Point2D:
        """Orthogonally project a point onto an infinite line."""
        dx = line.end.x-line.start.x
        dy = line.end.y-line.start.y
        denom = dx*dx+dy*dy
        if denom == 0:
            raise ValueError("degenerate_line")
        t = ((point.x-line.start.x)*dx+(point.y-line.start.y)*dy)/denom
        return Point2D(line.start.x+t*dx,line.start.y+t*dy)
