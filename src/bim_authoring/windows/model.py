from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Mapping

class WindowOperation(str, Enum):
    FIXED = "fixed"
    CASEMENT = "casement"
    AWNING = "awning"
    SLIDING = "sliding"

@dataclass(frozen=True, slots=True)
class WindowGlass:
    glass_id: str
    material_id: str
    thickness: float
    u_value: float
    solar_heat_gain_coefficient: float

    def __post_init__(self):
        if not self.glass_id.strip() or not self.material_id.strip():
            raise ValueError("glass_id y material_id son obligatorios")
        if self.thickness <= 0 or self.u_value <= 0:
            raise ValueError("Propiedades de vidrio inválidas")
        if not 0 <= self.solar_heat_gain_coefficient <= 1:
            raise ValueError("SHGC inválido")

@dataclass(frozen=True, slots=True)
class WindowFrame:
    frame_id: str
    material_id: str
    depth: float
    face_width: float

    def __post_init__(self):
        if not self.frame_id.strip() or not self.material_id.strip():
            raise ValueError("frame_id y material_id son obligatorios")
        if self.depth <= 0 or self.face_width <= 0:
            raise ValueError("Dimensiones de marco inválidas")

@dataclass(frozen=True, slots=True)
class WindowType:
    type_id: str
    name: str
    width: float
    height: float
    operation: WindowOperation
    frame: WindowFrame
    glass: WindowGlass
    mullion_count_vertical: int = 0
    mullion_count_horizontal: int = 0

    def __post_init__(self):
        if not self.type_id.strip() or not self.name.strip():
            raise ValueError("type_id y name son obligatorios")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensiones de ventana inválidas")
        if self.mullion_count_vertical < 0 or self.mullion_count_horizontal < 0:
            raise ValueError("Conteo de montantes inválido")

@dataclass(frozen=True, slots=True)
class WindowFamily:
    family_id: str
    name: str
    types: tuple[WindowType, ...]

    def __post_init__(self):
        if not self.family_id.strip() or not self.name.strip():
            raise ValueError("family_id y name son obligatorios")
        if not self.types:
            raise ValueError("La familia requiere tipos")

    def get_type(self, type_id: str) -> WindowType:
        for window_type in self.types:
            if window_type.type_id == type_id:
                return window_type
        raise KeyError(type_id)

@dataclass(frozen=True, slots=True)
class WindowInstance:
    window_id: str
    family_id: str
    window_type: WindowType
    host_wall_id: str
    offset: float
    sill_height: float
    level_id: str | None = None
    flip_facing: bool = False
    properties: Mapping[str, Any] = field(default_factory=dict)
    revision: int = 0

    def __post_init__(self):
        if not self.window_id.strip() or not self.family_id.strip() or not self.host_wall_id.strip():
            raise ValueError("IDs obligatorios")
        if self.offset < 0 or self.sill_height < 0:
            raise ValueError("Posición inválida")

    def move(self, *, offset: float | None = None, sill_height: float | None = None):
        return replace(
            self,
            offset=self.offset if offset is None else float(offset),
            sill_height=self.sill_height if sill_height is None else float(sill_height),
            revision=self.revision + 1,
        )

    def change_type(self, window_type: WindowType):
        return replace(self, window_type=window_type, revision=self.revision + 1)
