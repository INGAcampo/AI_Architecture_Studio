"""
AI Architecture Studio
CAD Rectangle Object

CAD Professional Sprint 1
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

        self.set_property("Puntos", len(polyline.points))
        self.set_property("Cerrado", True)