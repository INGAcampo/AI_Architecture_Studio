"""
AI Architecture Studio
Beam Object

Foundation 1.6
"""

from models.base_object import BaseObject


class Beam(BaseObject):
    def __init__(self):
        super().__init__(
            name="Viga",
            object_type="Beam"
        )

        self.width = 0.30
        self.height = 0.50
        self.length = 3.00

        self.material = "Concreto"
        self.level = "Nivel 1"
        self.ifc_class = "IfcBeam"

        self.set_property("Ancho", self.width)
        self.set_property("Altura", self.height)
        self.set_property("Longitud", self.length)
        self.set_property("Material", self.material)
        self.set_property("Nivel", self.level)
        self.set_property("IFC", self.ifc_class)