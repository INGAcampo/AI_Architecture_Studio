from dataclasses import dataclass
from math import hypot
@dataclass(frozen=True,slots=True)
class CombinedWeldStressResult: shear_stress:float; normal_stress:float; equivalent_stress:float; ratio:float; passed:bool
class CombinedWeldStressEngine:
    def calculate(self,shear,tension,area,strength):
        ss=abs(shear)/max(area,1e-12); ns=abs(tension)/max(area,1e-12); eq=hypot(ss,ns); r=eq/max(strength,1e-12)
        return CombinedWeldStressResult(ss,ns,eq,r,r<=1)
