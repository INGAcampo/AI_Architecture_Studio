"""
AI Architecture Studio
CAD Circle Object

Foundation 4.1
"""

from engines.geometry.point import Point
from models.base_object import BaseObject


class CadCircle(BaseObject):

    def __init__(self, center, radius):
        super().__init__(
            name="Círculo CAD",
            object_type="CadCircle"
        )

        self.center = center
        self.radius = float(radius)

        self._update_properties()

    def _update_properties(self):
        self.properties.clear()

        self.set_property(
            "Centro",
            (
                round(self.center.x, 3),
                round(self.center.y, 3),
                round(self.center.z, 3),
            )
        )

        self.set_property(
            "Radio",
            round(self.radius, 3)
        )

        self.set_property(
            "Diámetro",
            round(self.radius * 2, 3)
        )

    def clone(self):
        cloned_center = Point(
            self.center.x,
            self.center.y,
            self.center.z,
        )

        return CadCircle(
            center=cloned_center,
            radius=self.radius,
        )