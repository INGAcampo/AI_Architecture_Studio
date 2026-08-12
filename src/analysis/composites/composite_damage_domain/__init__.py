from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class CompositeDamageState: fiber_damage:float; matrix_damage:float; shear_damage:float; delamination_damage:float; failed:bool
@dataclass(frozen=True,slots=True)
class CompositeDamageResult: state:CompositeDamageState; failure_index:float; iterations:int; converged:bool
