"""
AI Architecture Studio
CAD Line Object

Foundation 4.1
"""

from engines.geometry.line import Line
from engines.geometry.point import Point
from models.base_object import BaseObject


class CadLine(BaseObject):
    def __init__(self, geometry):
        super().__init__(
            name="Línea CAD",
            object_type="CadLine"
        )

        self.geometry = geometry
        self._update_properties()

    def _update_properties(self):
        self.properties.clear()

        self.set_property(
            "Longitud",
            round(self.geometry.length, 3)
        )
        self.set_property(
            "Inicio",
            self.geometry.start.to_tuple()
        )
        self.set_property(
            "Fin",
            self.geometry.end.to_tuple()
        )

    def clone(self):
        start = Point(
            self.geometry.start.x,
            self.geometry.start.y,
            self.geometry.start.z,
        )

        end = Point(
            self.geometry.end.x,
            self.geometry.end.y,
            self.geometry.end.z,
        )

        return CadLine(
            Line(start, end)
        )