from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ContinuityPlateResult:
    required_force:float; provided_capacity:float; ratio:float; required:bool; passed:bool
class ContinuityPlateEngine:
    def design(self,flange_force,column_capacity,plate_capacity):
        req=max(0,abs(flange_force)-column_capacity); r=req/max(plate_capacity,1e-12)
        return ContinuityPlateResult(req,plate_capacity,r,req>0,r<=1)
