from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ContactLoadStep: step:int; load_factor:float; penetration:float; residual:float; converged:bool
