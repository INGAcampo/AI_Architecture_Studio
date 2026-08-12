from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite, sqrt
from typing import Any

class CirculationKind(str, Enum):
    STRAIGHT_STAIR="straight_stair"; L_STAIR="l_stair"; U_STAIR="u_stair"; SPIRAL_STAIR="spiral_stair"; RAMP="ramp"

@dataclass(slots=True)
class IntelligentCirculation:
    circulation_id: str
    kind: CirculationKind
    base_elevation: float
    top_elevation: float
    width: float
    riser_height: float = 0.175
    tread_depth: float = 0.28
    run_length: float | None = None
    landing_count: int = 0
    handrail_height: float = 0.90
    revision: int = 0
    metadata: dict[str,Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.circulation_id.strip(): raise ValueError("circulation_id obligatorio")
        if self.top_elevation <= self.base_elevation: raise ValueError("top_elevation debe ser mayor")
        if min(self.width,self.riser_height,self.tread_depth,self.handrail_height)<=0: raise ValueError("Dimensiones positivas requeridas")
        if self.landing_count<0: raise ValueError("landing_count inválido")
    @property
    def rise(self): return self.top_elevation-self.base_elevation
    @property
    def riser_count(self): return max(1, round(self.rise/self.riser_height))
    @property
    def actual_riser_height(self): return self.rise/self.riser_count
    @property
    def tread_count(self): return max(0,self.riser_count-1)
    @property
    def calculated_run(self): return self.tread_count*self.tread_depth if self.run_length is None else self.run_length
    @property
    def slope(self): return self.rise/self.calculated_run if self.calculated_run else float("inf")
    @property
    def path_length(self): return sqrt(self.rise**2+self.calculated_run**2)
    def touch(self): self.revision+=1; return self.revision
