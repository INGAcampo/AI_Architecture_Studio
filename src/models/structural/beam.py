from __future__ import annotations

from math import dist
from typing import Iterable, Optional


class Beam:
    """Structural beam model with backward-compatible geometry inputs."""

    RECTANGULAR = "rectangular"
    STEEL = "steel"

    def __init__(
        self,
        start_point: Optional[Iterable[float]] = None,
        end_point: Optional[Iterable[float]] = None,
        **properties,
    ):
        self.name = properties.pop("name", "Viga")
        self.level = properties.pop("level", "Nivel 1")
        self.beam_type = properties.pop("beam_type", self.RECTANGULAR)
        self.material = properties.pop("material", "Concreto armado")
        self.concrete_strength_mpa = float(properties.pop("concrete_strength_mpa", 25.0))
        self.steel_grade = properties.pop("steel_grade", "Fy 420 MPa")
        self.profile = properties.pop("profile", "25x50 cm")
        self.cover_cm = float(properties.pop("cover_cm", 4.0))
        self.design_code = properties.pop("design_code", "")
        self.unit_system = properties.pop("unit_system", "metric_decimal")
        self.density_kg_m3 = float(properties.pop("density_kg_m3", 2400.0))

        self.start_point = self._point(start_point) if start_point is not None else None
        self.end_point = self._point(end_point) if end_point is not None else None

        explicit_length = properties.pop("length", None)
        if self.start_point is not None and self.end_point is not None:
            self.length = float(dist(self.start_point, self.end_point))
        else:
            self.length = float(explicit_length or 0.0)

        self.volume = float(properties.pop("volume", 0.0))
        self.properties = dict(properties.pop("properties", {}))
        self.properties.update(properties)

    @staticmethod
    def _point(value: Iterable[float]) -> tuple[float, ...]:
        point = tuple(float(component) for component in value)
        if len(point) not in (2, 3):
            raise ValueError("A beam point must contain two or three coordinates.")
        return point
