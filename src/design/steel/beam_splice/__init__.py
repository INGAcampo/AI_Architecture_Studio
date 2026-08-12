from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class BeamSpliceResult:
    flange_force:float; flange_ratio:float; web_ratio:float; unity_ratio:float; passed:bool
class BeamSpliceEngine:
    def design(self,moment,depth,flange_cap,shear,web_cap):
        f=abs(moment)/max(depth,1e-12); a=f/flange_cap; b=abs(shear)/web_cap; u=max(a,b)
        return BeamSpliceResult(f,a,b,u,u<=1)
