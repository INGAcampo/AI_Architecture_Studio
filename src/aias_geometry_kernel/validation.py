"""Finite-coordinate and geometric-domain validation for kernel entities."""
from __future__ import annotations
import math
from .primitives import Point2D, Line2D, Circle2D
from .polygon import Polygon2D

class GeometryValidationEngine:
    """Collect invalid coordinates, degenerate dimensions and unsupported geometry issues."""
    def validate(self, obj):
        """Collect finite-coordinate and domain violations for supported geometry."""
        issues=[]
        if isinstance(obj, Point2D):
            if not all(math.isfinite(v) for v in (obj.x,obj.y)):
                issues.append("non_finite_point")
        elif isinstance(obj, Line2D):
            if obj.length <= 0:
                issues.append("degenerate_line")
        elif isinstance(obj, Circle2D):
            if obj.radius <= 0:
                issues.append("invalid_radius")
        elif isinstance(obj, Polygon2D):
            if obj.area <= 0:
                issues.append("degenerate_polygon")
        else:
            issues.append("unsupported_geometry")
        return issues
