"""
AI Architecture Studio
CAD Arc Object — Package 4.1.1
"""

import math
from engines.geometry.point import Point
from models.base_object import BaseObject


class CadArc(BaseObject):

    def __init__(
        self,
        center,
        radius,
        start_angle,
        end_angle,
        clockwise=False,
    ):
        super().__init__(name="Arco CAD", object_type="CadArc")
        self.center = center
        self.radius = float(radius)
        self.start_angle = float(start_angle)
        self.end_angle = float(end_angle)
        self.clockwise = bool(clockwise)
        self.geometry = self

    @property
    def sweep_angle(self):
        if self.clockwise:
            return -(
                (self.start_angle - self.end_angle)
                % math.tau
            )

        return (
            self.end_angle - self.start_angle
        ) % math.tau

    @property
    def start_point(self):
        return Point(
            self.center.x + self.radius * math.cos(self.start_angle),
            self.center.y + self.radius * math.sin(self.start_angle),
            self.center.z,
        )

    @property
    def end_point(self):
        return Point(
            self.center.x + self.radius * math.cos(self.end_angle),
            self.center.y + self.radius * math.sin(self.end_angle),
            self.center.z,
        )

    def point_at(self, fraction):
        angle = self.start_angle + self.sweep_angle * fraction
        return Point(
            self.center.x + self.radius * math.cos(angle),
            self.center.y + self.radius * math.sin(angle),
            self.center.z,
        )

    def clone(self):
        return CadArc(
            Point(self.center.x, self.center.y, self.center.z),
            self.radius,
            self.start_angle,
            self.end_angle,
            self.clockwise,
        )
