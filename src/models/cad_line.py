"""
AI Architecture Studio
CAD Line Object

Foundation 2.0
"""

from models.base_object import BaseObject


class CadLine(BaseObject):
    def __init__(self, geometry):
        super().__init__(
            name="Línea CAD",
            object_type="CadLine"
        )

        self.geometry = geometry

        self.set_property("Longitud", round(geometry.length, 3))
        self.set_property("Inicio", geometry.start.to_tuple())
        self.set_property("Fin", geometry.end.to_tuple())