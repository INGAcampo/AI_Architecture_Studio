"""
AI Architecture Studio
Wall Object

Foundation 1.6
"""

from models.base_object import BaseObject


class Wall(BaseObject):
    def __init__(self):
        super().__init__(
            name="Muro",
            object_type="Wall"
        )

        # Propiedades geométricas
        self.thickness = 0.20      # metros
        self.height = 3.00         # metros

        # Material
        self.material = "Concreto"

        # Nivel
        self.level = "Nivel 1"

        # Clasificación BIM
        self.ifc_class = "IfcWall"

        # Registrar propiedades
        self.set_property("Espesor", self.thickness)
        self.set_property("Altura", self.height)
        self.set_property("Material", self.material)
        self.set_property("Nivel", self.level)
        self.set_property("IFC", self.ifc_class)