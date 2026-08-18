"""
AI Architecture Studio
CAD Rectangle Object

Foundation 4.1 / Dynamic Input 3.2
"""

from models.base_object import BaseObject


class CadRectangle(BaseObject):

    def __init__(
        self,
        polyline,
        width=None,
        height=None,
        angle_degrees=0.0,
    ):
        super().__init__(
            name="Rectángulo CAD",
            object_type="CadRectangle",
        )

        self.polyline = polyline
        self.geometry = polyline

        self.width = width
        self.height = height
        self.angle_degrees = float(
            angle_degrees or 0.0
        )

        self._update_properties()

    def _update_properties(self):
        self.properties.clear()

        self.set_property(
            "Puntos",
            len(self.polyline.points),
        )

        self.set_property(
            "Cerrado",
            self.polyline.closed,
        )

        if self.width is not None:
            self.set_property(
                "Ancho",
                self.width,
            )

        if self.height is not None:
            self.set_property(
                "Alto",
                self.height,
            )

        self.set_property(
            "Ángulo",
            self.angle_degrees,
        )

    def clone(self):
        return CadRectangle(
            self.polyline.clone(),
            width=self.width,
            height=self.height,
            angle_degrees=self.angle_degrees,
        )
