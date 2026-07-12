"""
AI Architecture Studio
CAD Polyline Object

CAD Professional Sprint 1
"""

from models.base_object import BaseObject


class CadPolyline(BaseObject):
    def __init__(self):
        super().__init__(
            name="Polilínea CAD",
            object_type="CadPolyline"
        )

        self.points = []
        self.closed = False

    def add_point(self, point):
        self.points.append(point)

    def close(self):
        self.closed = True

    @property
    def segment_count(self):
        if len(self.points) < 2:
            return 0

        if self.closed:
            return len(self.points)

        return len(self.points) - 1

    def info(self):
        data = super().info()
        data["Puntos"] = len(self.points)
        data["Segmentos"] = self.segment_count
        data["Cerrada"] = self.closed
        return data