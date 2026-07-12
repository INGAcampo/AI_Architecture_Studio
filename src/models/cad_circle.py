"""
AI Architecture Studio
CAD Circle Object

Foundation 3.3
"""

from models.base_object import BaseObject


class CadCircle(BaseObject):

    def __init__(self, center, radius):
        super().__init__(
            name="Círculo CAD",
            object_type="CadCircle"
        )

        self.center = center
        self.radius = radius

        self.set_property(
            "Centro",
            f"({center.x:.2f}, {center.y:.2f})"
        )

        self.set_property(
            "Radio",
            round(radius, 3)
        )

        self.set_property(
            "Diámetro",
            round(radius * 2, 3)
        )