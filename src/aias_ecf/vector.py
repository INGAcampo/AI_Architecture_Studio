"""Dependency-free vector arithmetic with explicit dimensional validation."""
from __future__ import annotations
import math

class VectorEngine:
    """Provide addition, subtraction, products, norm and scaling for numeric vectors."""
    @staticmethod
    def add(a, b):
        """Add equal-length vectors component by component."""
        if len(a) != len(b): raise ValueError("dimension_mismatch")
        return [x + y for x, y in zip(a, b)]

    @staticmethod
    def subtract(a, b):
        """Subtract equal-length vectors component by component."""
        if len(a) != len(b): raise ValueError("dimension_mismatch")
        return [x - y for x, y in zip(a, b)]

    @staticmethod
    def dot(a, b):
        """Return the dot product of equal-length vectors."""
        if len(a) != len(b): raise ValueError("dimension_mismatch")
        return sum(x * y for x, y in zip(a, b))

    @staticmethod
    def norm(a):
        """Return the Euclidean norm of a numeric vector."""
        return math.sqrt(sum(x * x for x in a))

    @staticmethod
    def scale(a, factor):
        """Multiply every vector component by a scalar factor."""
        return [factor * x for x in a]

    @staticmethod
    def cross(a, b):
        """Return the three-dimensional cross product of two 3-vectors."""
        if len(a) != 3 or len(b) != 3:
            raise ValueError("cross_requires_3d")
        return [
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0],
        ]
