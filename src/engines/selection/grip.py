"""
AI Architecture Studio
Grip Model

Professional Grips v1
"""

from dataclasses import dataclass

from engines.geometry.point import Point


@dataclass
class Grip:
    owner: object
    point: Point
    grip_type: str
    index: int | None = None
    active: bool = False
    hovered: bool = False

    def clone_point(self):
        return Point(
            self.point.x,
            self.point.y,
            self.point.z,
        )

    def set_point(self, point):
        self.point = Point(
            point.x,
            point.y,
            point.z,
        )

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def set_hovered(self, hovered):
        self.hovered = bool(hovered)