from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any

class FoundationKind(str, Enum):
    ISOLATED = "isolated"
    COMBINED = "combined"
    STRIP = "strip"
    MAT = "mat"
    PILE_CAP = "pile_cap"
    PILE = "pile"
    PEDESTAL = "pedestal"

@dataclass(frozen=True, slots=True)
class FoundationMaterial:
    material_id: str
    name: str
    density: float
    compressive_strength: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.material_id.strip() or not self.name.strip():
            raise ValueError("Identificadores obligatorios")
        if self.density <= 0:
            raise ValueError("density debe ser positiva")

@dataclass(slots=True)
class IntelligentFoundation:
    foundation_id: str
    kind: FoundationKind
    material_id: str
    length: float
    width: float
    depth: float
    elevation: float = 0.0
    supported_ids: tuple[str, ...] = ()
    soil_bearing_capacity: float | None = None
    revision: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.foundation_id.strip() or not self.material_id.strip():
            raise ValueError("Identificadores obligatorios")
        if min(self.length, self.width, self.depth) <= 0:
            raise ValueError("Dimensiones positivas requeridas")
        if not all(isfinite(v) for v in (self.length, self.width, self.depth, self.elevation)):
            raise ValueError("Dimensiones finitas requeridas")
        if self.soil_bearing_capacity is not None and self.soil_bearing_capacity <= 0:
            raise ValueError("soil_bearing_capacity debe ser positiva")
    @property
    def plan_area(self): return self.length * self.width
    @property
    def volume(self): return self.plan_area * self.depth
    @property
    def centroid(self): return (self.length/2, self.width/2, self.elevation - self.depth/2)
    def touch(self): self.revision += 1; return self.revision
