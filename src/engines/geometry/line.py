"""
AI Architecture Studio
Geometry Engine - Line
"""

from .point import Point


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    @property
    def length(self):
        return self.start.distance_to(self.end)

    @property
    def midpoint(self):
        return Point(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
            (self.start.z + self.end.z) / 2,
        )

    def __repr__(self):
        return f"Line({self.start}, {self.end})"