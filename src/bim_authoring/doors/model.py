from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Mapping, Any

class DoorOperation(str, Enum):
    SINGLE_SWING = "single_swing"
    DOUBLE_SWING = "double_swing"
    SLIDING = "sliding"
    FOLDING = "folding"

class DoorHanding(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    DOUBLE = "double"

@dataclass(frozen=True, slots=True)
class DoorPanel:
    panel_id: str
    material_id: str
    thickness: float

    def __post_init__(self):
        if not self.panel_id.strip() or not self.material_id.strip():
            raise ValueError("panel_id y material_id son obligatorios")
        if self.thickness <= 0:
            raise ValueError("thickness debe ser positiva")

@dataclass(frozen=True, slots=True)
class DoorFrame:
    frame_id: str
    material_id: str
    jamb_depth: float
    head_height: float

    def __post_init__(self):
        if not self.frame_id.strip() or not self.material_id.strip():
            raise ValueError("frame_id y material_id son obligatorios")
        if self.jamb_depth <= 0 or self.head_height <= 0:
            raise ValueError("Dimensiones de marco inválidas")

@dataclass(frozen=True, slots=True)
class DoorType:
    type_id: str
    name: str
    width: float
    height: float
    operation: DoorOperation
    handing: DoorHanding
    panel: DoorPanel
    frame: DoorFrame
    fire_rating_minutes: int = 0
    acoustic_rating_db: float = 0.0

    def __post_init__(self):
        if not self.type_id.strip() or not self.name.strip():
            raise ValueError("type_id y name son obligatorios")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensiones de puerta inválidas")
        if self.fire_rating_minutes < 0 or self.acoustic_rating_db < 0:
            raise ValueError("Ratings inválidos")

@dataclass(frozen=True, slots=True)
class DoorFamily:
    family_id: str
    name: str
    types: tuple[DoorType, ...]

    def __post_init__(self):
        if not self.family_id.strip() or not self.name.strip():
            raise ValueError("family_id y name son obligatorios")
        if not self.types:
            raise ValueError("La familia requiere tipos")

    def get_type(self, type_id: str) -> DoorType:
        for door_type in self.types:
            if door_type.type_id == type_id:
                return door_type
        raise KeyError(type_id)

@dataclass(frozen=True, slots=True)
class DoorInstance:
    door_id: str
    family_id: str
    door_type: DoorType
    host_wall_id: str
    offset: float
    sill_height: float = 0.0
    flip_facing: bool = False
    flip_hand: bool = False
    level_id: str | None = None
    properties: Mapping[str, Any] = field(default_factory=dict)
    revision: int = 0

    def __post_init__(self):
        if not self.door_id.strip() or not self.family_id.strip() or not self.host_wall_id.strip():
            raise ValueError("IDs obligatorios")
        if self.offset < 0 or self.sill_height < 0:
            raise ValueError("Posición inválida")

    def move(self, offset: float):
        return replace(self, offset=float(offset), revision=self.revision + 1)

    def change_type(self, door_type: DoorType):
        return replace(self, door_type=door_type, revision=self.revision + 1)
