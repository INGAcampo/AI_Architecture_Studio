"""AIAS Architectural Wall
Architectural Core 5.0.5.2.1 — DOOR History Fix.
"""

from engines.geometry.line import Line
from engines.geometry.point import Point
from models.base_object import BaseObject


class Wall(BaseObject):
    def __init__(
        self,
        path=None,
        thickness=0.20,
        justification="center",
        base_level="Nivel 0",
        height=3.00,
    ):
        super().__init__(name="Muro", object_type="Wall")
        self.path = [
            Point(p.x, p.y, getattr(p, "z", 0.0))
            for p in (path or [])
        ]
        self.thickness = float(thickness)
        self.justification = str(justification)
        self.base_level = str(base_level)
        self.height = float(height)
        self.visible = True

        self.geometry = None
        self.centerline = []
        self.exterior_edges = []
        self.interior_edges = []
        self.clean_polygon = []

        self.wall_node_ids = []
        self.wall_connections = []
        self.wall_network_revision = 0

        # Huecos alojados: base para puertas y ventanas.
        self.openings = []

        self._rebuild_geometry()
        self.rebuild_wall_geometry()
        self._update_properties()

    def _rebuild_geometry(self):
        self.geometry = (
            Line(self.path[0], self.path[-1])
            if len(self.path) >= 2
            else None
        )

    def rebuild_wall_geometry(self):
        from engines.architectural.wall_engine import WallEngine
        data = WallEngine.build_wall_data(self)
        self.centerline = data["centerline"]
        self.exterior_edges = data["left"]
        self.interior_edges = data["right"]
        self.clean_polygon = data["polygon"]

    @property
    def length(self):
        return sum(
            self.path[index].distance_to(self.path[index + 1])
            for index in range(len(self.path) - 1)
        )

    @property
    def segment_count(self):
        return max(0, len(self.path) - 1)

    @property
    def area_2d(self):
        gross = self.length * self.thickness
        removed = sum(
            min(opening.width, self.length) * self.thickness
            for opening in self.openings
        )
        return max(0.0, gross - removed)

    @property
    def opening_count(self):
        identifiers = set()
        anonymous = 0

        for opening in self.openings:
            opening_id = getattr(
                opening,
                "opening_id",
                None,
            )
            if opening_id is None:
                anonymous += 1
            else:
                identifiers.add(opening_id)

        return len(identifiers) + anonymous

    @property
    def door_count(self):
        identifiers = set()
        anonymous = 0

        for opening in self.openings:
            door = getattr(
                opening,
                "door",
                None,
            )
            if door is None:
                continue

            door_id = getattr(
                door,
                "door_id",
                None,
            )
            if door_id is None:
                anonymous += 1
            else:
                identifiers.add(door_id)

        return len(identifiers) + anonymous

    def set_path(self, points):
        self.path = [
            Point(p.x, p.y, getattr(p, "z", 0.0))
            for p in points
        ]
        self._rebuild_geometry()
        self.rebuild_wall_geometry()

        from engines.architectural.opening_engine import OpeningEngine
        OpeningEngine.update_after_wall_change(self)

        self._update_properties()

    def set_thickness(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("El espesor debe ser mayor que cero.")
        self.thickness = value
        self.rebuild_wall_geometry()
        self._update_properties()

    def add_opening(self, opening):
        from engines.architectural.opening_engine import OpeningEngine
        return OpeningEngine.add_to_wall(self, opening)

    def remove_opening(self, opening):
        from engines.architectural.opening_engine import OpeningEngine
        OpeningEngine.remove_from_wall(self, opening)

    def clone(self):
        clone = Wall(
            self.path,
            self.thickness,
            self.justification,
            self.base_level,
            self.height,
        )
        clone.layer_name = self.layer_name
        clone.openings = [
            opening.clone(host_wall=clone)
            for opening in self.openings
        ]
        clone._update_properties()
        return clone

    def _update_properties(self):
        self.properties.clear()
        values = {
            "Espesor": round(self.thickness, 3),
            "Altura": round(self.height, 3),
            "Longitud": round(self.length, 3),
            "Área neta en planta": round(self.area_2d, 3),
            "Justificación": self.justification,
            "Nivel base": self.base_level,
            "Segmentos": self.segment_count,
            "WALL JOIN": "Activo",
            "Nodos WALL": len(self.wall_node_ids),
            "Red WALL": self.wall_network_revision,
            "Huecos": self.opening_count,
            "Puertas": self.door_count,
            "Opening Core": "5.0.5.2.1",
            "Door Core": "5.0.5.2.1",
        }
        for key, value in values.items():
            self.set_property(key, value)

    def info(self):
        data = super().info()
        data.update(
            {
                "Longitud": round(self.length, 3),
                "Espesor": round(self.thickness, 3),
                "Altura": round(self.height, 3),
                "Área neta en planta": round(self.area_2d, 3),
                "Segmentos": self.segment_count,
                "WALL JOIN": "5.0.4.4",
                "Nodos WALL": len(self.wall_node_ids),
                "Red WALL": self.wall_network_revision,
                "Huecos": self.opening_count,
                "Puertas": self.door_count,
                "Opening Core": "5.0.5.2.1",
                "Door Core": "5.0.5.2.1",
            }
        )
        return data
