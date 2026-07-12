"""
AI Architecture Studio
Column Object

Foundation 1.6
"""

from models.base_object import BaseObject


class Column(BaseObject):
    def __init__(self):
        super().__init__(
            name="Columna",
            object_type="Column"
        )

        self.width = 0.30
        self.depth = 0.30
        self.height = 3.00

        self.material = "Concreto"
        self.level = "Nivel 1"
        self.ifc_class = "IfcColumn"

        self.set_property("Ancho", self.width)
        self.set_property("Profundidad", self.depth)
        self.set_property("Altura", self.height)
        self.set_property("Material", self.material)
        self.set_property("Nivel", self.level)
        self.set_property("IFC", self.ifc_class)