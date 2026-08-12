from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any


class OpeningKind(str, Enum):
    DOOR = "door"
    WINDOW = "window"
    GENERIC = "generic"


class OpeningState(str, Enum):
    ACTIVE = "active"
    SUPPRESSED = "suppressed"
    ORPHANED = "orphaned"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class OpeningPlacement:
    offset: float
    sill_height: float = 0.0
    flip_horizontal: bool = False
    flip_vertical: bool = False

    def __post_init__(self) -> None:
        if not all(isfinite(value) for value in (self.offset, self.sill_height)):
            raise ValueError("Los valores de ubicación deben ser finitos")


@dataclass(slots=True)
class Opening:
    opening_id: str
    host_wall_id: str
    kind: OpeningKind
    width: float
    height: float
    placement: OpeningPlacement
    name: str = ""
    type_id: str | None = None
    material_id: str | None = None
    state: OpeningState = OpeningState.ACTIVE
    revision: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.opening_id.strip():
            raise ValueError("opening_id no puede estar vacío")
        if not self.host_wall_id.strip():
            raise ValueError("host_wall_id no puede estar vacío")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width y height deben ser positivos")
        if not isfinite(self.width) or not isfinite(self.height):
            raise ValueError("width y height deben ser finitos")
        if not self.name:
            self.name = self.opening_id

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center_offset(self) -> float:
        return self.placement.offset + self.width / 2.0

    @property
    def head_height(self) -> float:
        return self.placement.sill_height + self.height

    def touch(self) -> int:
        self.revision += 1
        return self.revision

    def snapshot(self) -> dict[str, Any]:
        return {
            "opening_id": self.opening_id,
            "host_wall_id": self.host_wall_id,
            "kind": self.kind.value,
            "width": self.width,
            "height": self.height,
            "placement": {
                "offset": self.placement.offset,
                "sill_height": self.placement.sill_height,
                "flip_horizontal": self.placement.flip_horizontal,
                "flip_vertical": self.placement.flip_vertical,
            },
            "name": self.name,
            "type_id": self.type_id,
            "material_id": self.material_id,
            "state": self.state.value,
            "revision": self.revision,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class HostWallGeometry:
    wall_id: str
    length: float
    height: float
    thickness: float

    def __post_init__(self) -> None:
        if not self.wall_id.strip():
            raise ValueError("wall_id no puede estar vacío")
        if min(self.length, self.height, self.thickness) <= 0:
            raise ValueError("Las dimensiones del muro deben ser positivas")


@dataclass(frozen=True, slots=True)
class OpeningQuantities:
    gross_area: float
    opening_area: float
    net_area: float
    opening_volume: float
