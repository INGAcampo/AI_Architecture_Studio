from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import Enum
from math import hypot
from typing import Mapping, Any

class WallLocationLine(str, Enum):
    CENTERLINE = "centerline"
    FINISH_FACE_EXTERIOR = "finish_face_exterior"
    FINISH_FACE_INTERIOR = "finish_face_interior"
    CORE_CENTERLINE = "core_centerline"

@dataclass(frozen=True, slots=True)
class WallLayer:
    layer_id: str
    material_id: str
    thickness: float
    function: str = "finish"

    def __post_init__(self):
        if not self.layer_id.strip() or not self.material_id.strip():
            raise ValueError("layer_id y material_id son obligatorios")
        if self.thickness <= 0:
            raise ValueError("thickness debe ser positiva")

@dataclass(frozen=True, slots=True)
class CompoundStructure:
    layers: tuple[WallLayer, ...]

    def __post_init__(self):
        if not self.layers:
            raise ValueError("La estructura compuesta requiere capas")

    @property
    def total_thickness(self):
        return sum(layer.thickness for layer in self.layers)

@dataclass(frozen=True, slots=True)
class WallType:
    type_id: str
    name: str
    structure: CompoundStructure
    fire_rating_minutes: int = 0
    thermal_resistance: float = 0.0
    classification: str = "basic_wall"

    def __post_init__(self):
        if not self.type_id.strip() or not self.name.strip():
            raise ValueError("type_id y name son obligatorios")
        if self.fire_rating_minutes < 0 or self.thermal_resistance < 0:
            raise ValueError("Propiedades físicas inválidas")

@dataclass(frozen=True, slots=True)
class WallProfile:
    start: tuple[float, float, float]
    end: tuple[float, float, float]
    base_elevation: float
    height: float

    def __post_init__(self):
        if self.height <= 0:
            raise ValueError("height debe ser positiva")
        if self.length <= 0:
            raise ValueError("La longitud del muro debe ser positiva")

    @property
    def length(self):
        return hypot(self.end[0]-self.start[0], self.end[1]-self.start[1])

@dataclass(frozen=True, slots=True)
class WallInstance:
    wall_id: str
    wall_type: WallType
    profile: WallProfile
    location_line: WallLocationLine = WallLocationLine.CENTERLINE
    level_id: str | None = None
    properties: Mapping[str, Any] = field(default_factory=dict)
    revision: int = 0

    def __post_init__(self):
        if not self.wall_id.strip():
            raise ValueError("wall_id es obligatorio")

    def with_profile(self, profile: WallProfile):
        return replace(self, profile=profile, revision=self.revision + 1)

    def with_type(self, wall_type: WallType):
        return replace(self, wall_type=wall_type, revision=self.revision + 1)
