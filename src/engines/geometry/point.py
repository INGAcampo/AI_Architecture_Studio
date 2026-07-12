"""
AI Architecture Studio
Geometry Engine - Point
"""

import math


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_to(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"