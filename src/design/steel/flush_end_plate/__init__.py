from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class FlushEndPlateResult:
    bolt_force:float; plate_ratio:float; bolt_ratio:float; unity_ratio:float; passed:bool
class FlushEndPlateEngine:
    def design(self,moment,lever_arm,plate_cap,bolt_cap):
        f=abs(moment)/max(lever_arm,1e-12); a=f/plate_cap; b=f/bolt_cap; u=max(a,b)
        return FlushEndPlateResult(f,a,b,u,u<=1)
