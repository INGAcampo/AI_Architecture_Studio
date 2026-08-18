from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RCColumnInput:
    column_id:str; width:float; depth:float; length:float; concrete_strength:float; steel_yield_strength:float; steel_area:float; axial_load:float; moment_x:float; moment_y:float
@dataclass(frozen=True,slots=True)
class RCColumnResult:
    axial_capacity:float; moment_capacity_x:float; moment_capacity_y:float; interaction_ratio:float; slenderness_ratio:float; status:str
