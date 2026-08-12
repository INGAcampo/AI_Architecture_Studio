from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DirectWeldedMomentResult:
    flange_force:float; flange_weld_ratio:float; web_weld_ratio:float; unity_ratio:float; passed:bool
class DirectWeldedMomentEngine:
    def design(self,moment,beam_depth,flange_weld_cap,shear,web_weld_cap):
        f=abs(moment)/max(beam_depth,1e-12); a=f/flange_weld_cap; b=abs(shear)/web_weld_cap; u=max(a,b)
        return DirectWeldedMomentResult(f,a,b,u,u<=1)
