from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PryingActionResult:
    direct_tension:float; prying_force:float; total_bolt_tension:float; ratio:float; passed:bool
class PryingActionEngine:
    def calculate(self,direct_tension,plate_flexibility,bolt_capacity):
        q=abs(direct_tension)*max(plate_flexibility,0); total=abs(direct_tension)+q; r=total/max(bolt_capacity,1e-12)
        return PryingActionResult(direct_tension,q,total,r,r<=1)
