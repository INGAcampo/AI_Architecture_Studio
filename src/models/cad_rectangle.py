"""
AI Architecture Studio
CAD Rectangle Object

Foundation 4.1
"""

from models.base_object import BaseObject


class CadRectangle(BaseObject):
    def __init__(self, polyline):
        super().__init__(
            name="Rectángulo CAD",
            object_type="CadRectangle"
        )

        self.polyline = polyline
        self.geometry = polyline

        self._update_properties()

    def _update_properties(self):
        self.properties.clear()

        self.set_property(
            "Puntos",
            len(self.polyline.points)
        )

        self.set_property(
            "Cerrado",
            self.polyline.closed
        )

    def clone(self):
        return CadRectangle(
            self.polyline.clone()
        )