"""Typed soil, support, geometry and foundation-object domain contracts."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
from .enums import FoundationType, ShapeType

@dataclass(slots=True)
class SoilProfile:
    """Geotechnical parameters with explicit pressure, density, stiffness and depth units."""
    allowable_bearing_pressure_kpa: float
    unit_weight_kn_m3: float
    friction_angle_deg: float | None = None
    cohesion_kpa: float | None = None
    elastic_modulus_mpa: float | None = None
    groundwater_depth_m: float | None = None

@dataclass(slots=True)
class ColumnSupport:
    """Located column support carrying axial force and biaxial moments."""
    support_id: str
    x_m: float
    y_m: float
    width_m: float
    depth_m: float
    axial_load_kn: float
    moment_x_knm: float = 0.0
    moment_y_knm: float = 0.0

@dataclass(slots=True)
class FoundationGeometry:
    """Plan shape, principal dimensions, thickness and embedment of a foundation."""
    shape: ShapeType
    width_m: float
    length_m: float
    thickness_m: float
    embedment_m: float = 0.0

    @property
    def area_m2(self) -> float:
        """Return rectangular, square or circular plan area in square metres."""
        if self.shape in (ShapeType.RECTANGULAR, ShapeType.SQUARE):
            return self.width_m * self.length_m
        if self.shape == ShapeType.CIRCULAR:
            return 3.141592653589793 * (self.width_m / 2.0) ** 2
        raise ValueError("unsupported_shape")

    @property
    def volume_m3(self) -> float:
        """Return gross foundation volume as plan area times thickness."""
        return self.area_m2 * self.thickness_m

@dataclass(slots=True)
class FoundationObject:
    """Versioned foundation aggregate with materials, soil, supports and traceability."""
    object_id: str
    foundation_type: FoundationType
    name: str
    geometry: FoundationGeometry
    soil: SoilProfile
    supports: list[ColumnSupport]
    concrete_strength_mpa: float
    steel_yield_strength_mpa: float
    cover_m: float
    metadata: dict[str, Any] = field(default_factory=dict)
    traceability: dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"

    def to_dict(self) -> dict[str, Any]:
        """Serialize nested records and replace enum objects with stable values."""
        data = asdict(self)
        data["foundation_type"] = self.foundation_type.value
        data["geometry"]["shape"] = self.geometry.shape.value
        return data
