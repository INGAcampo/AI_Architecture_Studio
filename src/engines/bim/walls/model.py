from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from math import isfinite
from typing import Any


class WallLayerFunction(str, Enum):
    FINISH = "finish"
    SUBSTRATE = "substrate"
    INSULATION = "insulation"
    STRUCTURE = "structure"
    MEMBRANE = "membrane"
    AIR = "air"


class WallLocationLine(str, Enum):
    CENTERLINE = "centerline"
    CORE_CENTERLINE = "core_centerline"
    FINISH_FACE_EXTERIOR = "finish_face_exterior"
    FINISH_FACE_INTERIOR = "finish_face_interior"
    CORE_FACE_EXTERIOR = "core_face_exterior"
    CORE_FACE_INTERIOR = "core_face_interior"


@dataclass(frozen=True, slots=True)
class WallLayer:
    layer_id: str
    name: str
    function: WallLayerFunction
    thickness: float
    material_id: str | None = None
    priority: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.layer_id.strip():
            raise ValueError("layer_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if self.thickness < 0 or not isfinite(self.thickness):
            raise ValueError("thickness debe ser finito y no negativo")
        if self.function is not WallLayerFunction.MEMBRANE and self.thickness == 0:
            raise ValueError("Solo una membrana puede tener espesor cero")
        if self.priority < 0:
            raise ValueError("priority no puede ser negativa")


@dataclass(frozen=True, slots=True)
class CompoundStructure:
    layers: tuple[WallLayer, ...]

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("La estructura compuesta requiere capas")
        ids = [layer.layer_id for layer in self.layers]
        if len(ids) != len(set(ids)):
            raise KeyError("layer_id duplicado")

    @property
    def total_thickness(self) -> float:
        return sum(layer.thickness for layer in self.layers)

    @property
    def core_layers(self) -> tuple[WallLayer, ...]:
        return tuple(layer for layer in self.layers if layer.function is WallLayerFunction.STRUCTURE)

    @property
    def core_thickness(self) -> float:
        return sum(layer.thickness for layer in self.core_layers)

    def replace_layer(self, layer_id: str, new_layer: WallLayer) -> "CompoundStructure":
        found = False
        result = []
        for layer in self.layers:
            if layer.layer_id == layer_id:
                result.append(new_layer)
                found = True
            else:
                result.append(layer)
        if not found:
            raise KeyError(f"Capa desconocida: {layer_id}")
        return CompoundStructure(tuple(result))


@dataclass(frozen=True, slots=True)
class WallType:
    type_id: str
    name: str
    structure: CompoundStructure
    fire_rating_minutes: int = 0
    acoustic_rating_db: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.type_id.strip():
            raise ValueError("type_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if self.fire_rating_minutes < 0:
            raise ValueError("fire_rating_minutes no puede ser negativo")
        if self.acoustic_rating_db < 0:
            raise ValueError("acoustic_rating_db no puede ser negativo")

    def duplicate(self, new_type_id: str, new_name: str) -> "WallType":
        return replace(self, type_id=new_type_id, name=new_name)


@dataclass(slots=True)
class IntelligentWall:
    wall_id: str
    wall_type_id: str
    length: float
    base_elevation: float
    height: float
    location_line: WallLocationLine = WallLocationLine.CENTERLINE
    base_level_id: str | None = None
    top_level_id: str | None = None
    base_offset: float = 0.0
    top_offset: float = 0.0
    flipped: bool = False
    structural: bool = False
    revision: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.wall_id.strip():
            raise ValueError("wall_id no puede estar vacío")
        if not self.wall_type_id.strip():
            raise ValueError("wall_type_id no puede estar vacío")
        if self.length <= 0 or self.height <= 0:
            raise ValueError("length y height deben ser positivos")
        if not all(isfinite(v) for v in (
            self.length, self.base_elevation, self.height,
            self.base_offset, self.top_offset
        )):
            raise ValueError("Las dimensiones deben ser finitas")

    @property
    def top_elevation(self) -> float:
        return self.base_elevation + self.base_offset + self.height + self.top_offset

    def touch(self) -> int:
        self.revision += 1
        return self.revision
