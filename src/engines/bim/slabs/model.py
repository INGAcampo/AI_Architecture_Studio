from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any


class SlabLayerFunction(str, Enum):
    FINISH = "finish"
    SUBSTRATE = "substrate"
    INSULATION = "insulation"
    STRUCTURE = "structure"
    MEMBRANE = "membrane"


class SlabKind(str, Enum):
    FLOOR = "floor"
    FOUNDATION = "foundation"
    ROOF_DECK = "roof_deck"
    GENERIC = "generic"


@dataclass(frozen=True, slots=True)
class Point2D:
    x: float
    y: float

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.x, self.y)):
            raise ValueError("Las coordenadas deben ser finitas")


@dataclass(frozen=True, slots=True)
class SlabLayer:
    layer_id: str
    name: str
    function: SlabLayerFunction
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
        if self.function is not SlabLayerFunction.MEMBRANE and self.thickness == 0:
            raise ValueError("Solo una membrana puede tener espesor cero")
        if self.priority < 0:
            raise ValueError("priority no puede ser negativa")


@dataclass(frozen=True, slots=True)
class SlabStructure:
    layers: tuple[SlabLayer, ...]

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("La estructura de losa requiere capas")
        ids = [layer.layer_id for layer in self.layers]
        if len(ids) != len(set(ids)):
            raise KeyError("layer_id duplicado")

    @property
    def total_thickness(self) -> float:
        return sum(layer.thickness for layer in self.layers)

    @property
    def structural_thickness(self) -> float:
        return sum(
            layer.thickness
            for layer in self.layers
            if layer.function is SlabLayerFunction.STRUCTURE
        )


@dataclass(frozen=True, slots=True)
class SlabType:
    type_id: str
    name: str
    structure: SlabStructure
    kind: SlabKind = SlabKind.FLOOR
    load_capacity: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.type_id.strip():
            raise ValueError("type_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if self.load_capacity is not None and self.load_capacity < 0:
            raise ValueError("load_capacity no puede ser negativa")


@dataclass(frozen=True, slots=True)
class SlabOpening:
    opening_id: str
    boundary: tuple[Point2D, ...]

    def __post_init__(self) -> None:
        if not self.opening_id.strip():
            raise ValueError("opening_id no puede estar vacío")
        if len(self.boundary) < 3:
            raise ValueError("El hueco requiere al menos tres puntos")


@dataclass(slots=True)
class IntelligentSlab:
    slab_id: str
    slab_type_id: str
    boundary: tuple[Point2D, ...]
    elevation: float = 0.0
    level_id: str | None = None
    slope: float = 0.0
    slope_direction_degrees: float = 0.0
    openings: tuple[SlabOpening, ...] = ()
    structural: bool = True
    revision: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.slab_id.strip():
            raise ValueError("slab_id no puede estar vacío")
        if not self.slab_type_id.strip():
            raise ValueError("slab_type_id no puede estar vacío")
        if len(self.boundary) < 3:
            raise ValueError("El contorno requiere al menos tres puntos")
        if not all(isfinite(v) for v in (self.elevation, self.slope, self.slope_direction_degrees)):
            raise ValueError("Los valores geométricos deben ser finitos")
        if self.slope < 0:
            raise ValueError("slope no puede ser negativa")

    def touch(self) -> int:
        self.revision += 1
        return self.revision
