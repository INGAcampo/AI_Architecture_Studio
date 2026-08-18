from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class FinPlateResult:
    plate_shear_capacity:float; bolt_capacity:float; weld_capacity:float; unity_ratio:float; passed:bool
class FinPlateDesignEngine:
    def design(self,demand,plate_capacity,bolt_capacity,weld_capacity):
        cap=min(plate_capacity,bolt_capacity,weld_capacity)
        u=abs(demand)/max(cap,1e-12)
        return FinPlateResult(plate_capacity,bolt_capacity,weld_capacity,u,u<=1)
