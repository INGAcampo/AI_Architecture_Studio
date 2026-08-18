"""AI Architecture Studio
Architectural Core 5.0.8.4 — SLAB Structural Data.
"""

from uuid import uuid4

from engines.geometry.point import Point
from models.base_object import BaseObject


class Slab(BaseObject):
    """Losa BIM asociada a un ROOM con propiedades estructurales."""

    def __init__(
        self,
        host_room=None,
        boundary=None,
        thickness=0.15,
        material="Concreto armado",
        elevation=0.0,
        name=None,
        slab_id=None,
        concrete_strength_mpa=25.0,
        density_kg_m3=2400.0,
        superimposed_dead_load_kg_m2=100.0,
        live_load_kg_m2=200.0,
        finish_load_kg_m2=50.0,
    ):
        room_name = getattr(host_room, "name", "Ambiente")
        super().__init__(
            name=str(name or f"Losa - {room_name}"),
            object_type="Slab",
        )

        self.slab_id = str(slab_id or uuid4())
        self.host_room = host_room
        self.host_room_id = getattr(host_room, "room_id", None)

        self.thickness = max(0.001, float(thickness))
        self.material = str(material or "Concreto armado")
        self.elevation = float(elevation)

        self.concrete_strength_mpa = max(
            0.0,
            float(concrete_strength_mpa),
        )
        self.density_kg_m3 = max(0.0, float(density_kg_m3))
        self.superimposed_dead_load_kg_m2 = max(
            0.0,
            float(superimposed_dead_load_kg_m2),
        )
        self.live_load_kg_m2 = max(
            0.0,
            float(live_load_kg_m2),
        )
        self.finish_load_kg_m2 = max(
            0.0,
            float(finish_load_kg_m2),
        )

        self.visible = True
        self.valid = True

        source_boundary = (
            list(getattr(host_room, "boundary", []) or [])
            if host_room is not None
            else list(boundary or [])
        )

        self.boundary = []
        self.area = 0.0
        self.perimeter = 0.0
        self.volume = 0.0
        self.self_weight_kg_m2 = 0.0
        self.total_dead_load_kg_m2 = 0.0
        self.total_service_load_kg_m2 = 0.0
        self.total_self_weight_kg = 0.0
        self.total_service_load_kg = 0.0

        self.update_geometry(source_boundary)

    def update_geometry(self, boundary):
        from engines.architectural.room_engine import RoomEngine

        self.boundary = [
            Point(point.x, point.y, getattr(point, "z", 0.0))
            for point in (boundary or [])
        ]
        self.valid = len(self.boundary) >= 3
        self.area = RoomEngine.compute_area(self.boundary)
        self.perimeter = RoomEngine.compute_perimeter(self.boundary)
        self._recalculate()
        return self

    def _recalculate(self):
        self.volume = self.area * self.thickness
        self.self_weight_kg_m2 = (
            self.thickness * self.density_kg_m3
        )
        self.total_dead_load_kg_m2 = (
            self.self_weight_kg_m2
            + self.superimposed_dead_load_kg_m2
            + self.finish_load_kg_m2
        )
        self.total_service_load_kg_m2 = (
            self.total_dead_load_kg_m2
            + self.live_load_kg_m2
        )
        self.total_self_weight_kg = (
            self.self_weight_kg_m2 * self.area
        )
        self.total_service_load_kg = (
            self.total_service_load_kg_m2 * self.area
        )
        self._update_properties()

    def set_thickness(self, value):
        self.thickness = max(0.001, float(value))
        self._recalculate()

    def set_material(self, value):
        value = str(value or "").strip()
        if value:
            self.material = value
        self._update_properties()

    def set_elevation(self, value):
        self.elevation = float(value)
        self._update_properties()

    def set_concrete_strength(self, value):
        self.concrete_strength_mpa = max(0.0, float(value))
        self._update_properties()

    def set_density(self, value):
        self.density_kg_m3 = max(0.0, float(value))
        self._recalculate()

    def set_superimposed_dead_load(self, value):
        self.superimposed_dead_load_kg_m2 = max(
            0.0,
            float(value),
        )
        self._recalculate()

    def set_live_load(self, value):
        self.live_load_kg_m2 = max(0.0, float(value))
        self._recalculate()

    def set_finish_load(self, value):
        self.finish_load_kg_m2 = max(0.0, float(value))
        self._recalculate()

    def invalidate(self):
        self.valid = False
        self._update_properties()

    def data_snapshot(self):
        return {
            "thickness": self.thickness,
            "material": self.material,
            "elevation": self.elevation,
            "concrete_strength_mpa": self.concrete_strength_mpa,
            "density_kg_m3": self.density_kg_m3,
            "superimposed_dead_load_kg_m2": (
                self.superimposed_dead_load_kg_m2
            ),
            "live_load_kg_m2": self.live_load_kg_m2,
            "finish_load_kg_m2": self.finish_load_kg_m2,
        }

    def apply_data_snapshot(self, data):
        self.thickness = max(
            0.001,
            float(data.get("thickness", self.thickness)),
        )
        self.material = str(
            data.get("material", self.material)
        )
        self.elevation = float(
            data.get("elevation", self.elevation)
        )
        self.concrete_strength_mpa = max(
            0.0,
            float(
                data.get(
                    "concrete_strength_mpa",
                    self.concrete_strength_mpa,
                )
            ),
        )
        self.density_kg_m3 = max(
            0.0,
            float(
                data.get(
                    "density_kg_m3",
                    self.density_kg_m3,
                )
            ),
        )
        self.superimposed_dead_load_kg_m2 = max(
            0.0,
            float(
                data.get(
                    "superimposed_dead_load_kg_m2",
                    self.superimposed_dead_load_kg_m2,
                )
            ),
        )
        self.live_load_kg_m2 = max(
            0.0,
            float(
                data.get(
                    "live_load_kg_m2",
                    self.live_load_kg_m2,
                )
            ),
        )
        self.finish_load_kg_m2 = max(
            0.0,
            float(
                data.get(
                    "finish_load_kg_m2",
                    self.finish_load_kg_m2,
                )
            ),
        )
        self._recalculate()

    def clone(self):
        return Slab(
            host_room=self.host_room,
            boundary=self.boundary,
            thickness=self.thickness,
            material=self.material,
            elevation=self.elevation,
            name=self.name,
            concrete_strength_mpa=self.concrete_strength_mpa,
            density_kg_m3=self.density_kg_m3,
            superimposed_dead_load_kg_m2=(
                self.superimposed_dead_load_kg_m2
            ),
            live_load_kg_m2=self.live_load_kg_m2,
            finish_load_kg_m2=self.finish_load_kg_m2,
        )

    def _update_properties(self):
        room_name = getattr(self.host_room, "name", "-")
        values = {
            "Nombre": self.name,
            "Ambiente anfitrión": room_name,
            "Espesor": round(self.thickness, 4),
            "Material": self.material,
            "Elevación": round(self.elevation, 4),
            "Resistencia concreto": (
                f"{self.concrete_strength_mpa:g} MPa"
            ),
            "Densidad": f"{self.density_kg_m3:g} kg/m³",
            "Área": round(self.area, 3),
            "Perímetro": round(self.perimeter, 3),
            "Volumen": round(self.volume, 4),
            "Peso propio": (
                f"{self.self_weight_kg_m2:.2f} kg/m²"
            ),
            "Carga muerta adicional": (
                f"{self.superimposed_dead_load_kg_m2:.2f} kg/m²"
            ),
            "Carga de acabados": (
                f"{self.finish_load_kg_m2:.2f} kg/m²"
            ),
            "Sobrecarga de uso": (
                f"{self.live_load_kg_m2:.2f} kg/m²"
            ),
            "Carga muerta total": (
                f"{self.total_dead_load_kg_m2:.2f} kg/m²"
            ),
            "Carga de servicio": (
                f"{self.total_service_load_kg_m2:.2f} kg/m²"
            ),
            "Carga total losa": (
                f"{self.total_service_load_kg:.2f} kg"
            ),
            "Válida": "Sí" if self.valid else "No",
            "SLAB Core": "5.0.8.4",
        }

        self.properties.clear()
        setter = getattr(self, "set_property", None)
        for key, value in values.items():
            if callable(setter):
                setter(key, value)
            else:
                self.properties[key] = value

    def info(self):
        data = super().info()
        data.update(
            {
                "Ambiente anfitrión": getattr(
                    self.host_room,
                    "name",
                    "-",
                ),
                "Espesor": round(self.thickness, 4),
                "Material": self.material,
                "Elevación": round(self.elevation, 4),
                "Resistencia concreto": (
                    f"{self.concrete_strength_mpa:g} MPa"
                ),
                "Densidad": (
                    f"{self.density_kg_m3:g} kg/m³"
                ),
                "Área": round(self.area, 3),
                "Volumen": round(self.volume, 4),
                "Peso propio": (
                    f"{self.self_weight_kg_m2:.2f} kg/m²"
                ),
                "Carga muerta total": (
                    f"{self.total_dead_load_kg_m2:.2f} kg/m²"
                ),
                "Sobrecarga de uso": (
                    f"{self.live_load_kg_m2:.2f} kg/m²"
                ),
                "Carga de servicio": (
                    f"{self.total_service_load_kg_m2:.2f} kg/m²"
                ),
                "SLAB Core": "5.0.8.4",
            }
        )
        return data
