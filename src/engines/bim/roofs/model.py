from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any


class RoofKind(str, Enum):
    FLAT = "flat"
    SHED = "shed"
    GABLE = "gable"
    HIP = "hip"
    BUTTERFLY = "butterfly"
    GENERIC = "generic"


class RoofLayerFunction(str, Enum):
    FINISH = "finish"
    WATERPROOFING = "waterproofing"
    INSULATION = "insulation"
    STRUCTURE = "structure"
    MEMBRANE = "membrane"
    CEILING = "ceiling"


@dataclass(frozen=True, slots=True)
class RoofPoint:
    x: float
    y: float

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.x, self.y)):
            raise ValueError("Las coordenadas deben ser finitas")


@dataclass(frozen=True, slots=True)
class RoofLayer:
    layer_id: str
    name: str
    function: RoofLayerFunction
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
        if self.function is not RoofLayerFunction.MEMBRANE and self.thickness == 0:
            raise ValueError("Solo una membrana puede tener espesor cero")
        if self.priority < 0:
            raise ValueError("priority no puede ser negativa")


@dataclass(frozen=True, slots=True)
class RoofStructure:
    layers: tuple[RoofLayer, ...]

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("La estructura requiere capas")
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
            if layer.function is RoofLayerFunction.STRUCTURE
        )


@dataclass(frozen=True, slots=True)
class RoofType:
    type_id: str
    name: str
    structure: RoofStructure
    kind: RoofKind = RoofKind.GENERIC
    default_pitch_degrees: float = 0.0
    default_overhang: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.type_id.strip():
            raise ValueError("type_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if not 0 <= self.default_pitch_degrees < 90:
            raise ValueError("default_pitch_degrees debe estar entre 0 y 90")
        if self.default_overhang < 0:
            raise ValueError("default_overhang no puede ser negativo")


@dataclass(frozen=True, slots=True)
class RoofOpening:
    opening_id: str
    boundary: tuple[RoofPoint, ...]

    def __post_init__(self) -> None:
        if not self.opening_id.strip():
            raise ValueError("opening_id no puede estar vacío")
        if len(self.boundary) < 3:
            raise ValueError("El hueco requiere al menos tres puntos")


@dataclass(slots=True)
class IntelligentRoof:
    roof_id: str
    roof_type_id: str
    boundary: tuple[RoofPoint, ...]
    elevation: float = 0.0
    pitch_degrees: float = 0.0
    overhang: float = 0.0
    ridge_length: float = 0.0
    valley_length: float = 0.0
    hip_length: float = 0.0
    openings: tuple[RoofOpening, ...] = ()
    revision: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.roof_id.strip():
            raise ValueError("roof_id no puede estar vacío")
        if not self.roof_type_id.strip():
            raise ValueError("roof_type_id no puede estar vacío")
        if len(self.boundary) < 3:
            raise ValueError("El contorno requiere al menos tres puntos")
        if not 0 <= self.pitch_degrees < 90:
            raise ValueError("pitch_degrees debe estar entre 0 y 90")
        if self.overhang < 0:
            raise ValueError("overhang no puede ser negativo")
        if min(self.ridge_length, self.valley_length, self.hip_length) < 0:
            raise ValueError("Las longitudes auxiliares no pueden ser negativas")

    def touch(self) -> int:
        self.revision += 1
        return self.revision
