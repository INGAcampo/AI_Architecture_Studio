from dataclasses import dataclass
from enum import Enum
class WeldType(str,Enum): FILLET="fillet"; CJP="cjp"; PJP="pjp"
class ElectrodeClass(str,Enum): E60="E60"; E70="E70"; E80="E80"; E90="E90"
@dataclass(frozen=True,slots=True)
class WeldMaterial: electrode:ElectrodeClass; tensile_strength:float
@dataclass(frozen=True,slots=True)
class WeldSegment:
    segment_id:str; weld_type:WeldType; size:float; length:float
    x1:float; y1:float; x2:float; y2:float; material:WeldMaterial
@dataclass(frozen=True,slots=True)
class WeldDemand: force_x:float=0.; force_y:float=0.; tension:float=0.; moment:float=0.
@dataclass(frozen=True,slots=True)
class WeldDesignResult:
    segment_id:str; effective_throat:float; effective_area:float; design_capacity:float
    demand:float; unity_ratio:float; passed:bool; governing_check:str
