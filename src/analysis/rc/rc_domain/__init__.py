from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RCBeamInput:
    beam_id:str; width:float; depth:float; effective_depth:float; concrete_strength:float; steel_yield_strength:float; factored_moment:float; factored_shear:float
@dataclass(frozen=True,slots=True)
class RCBeamResult:
    steel_area:float; nominal_moment:float; design_moment:float; shear_capacity:float; utilization:float; status:str
