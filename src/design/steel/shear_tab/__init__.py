from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ShearTabResult:
    eccentricity:float; demand_moment:float; shear_ratio:float; moment_ratio:float; unity_ratio:float; passed:bool
class ShearTabEngine:
    def design(self,shear,eccentricity,shear_capacity,moment_capacity):
        m=abs(shear*eccentricity); vr=abs(shear)/max(shear_capacity,1e-12); mr=m/max(moment_capacity,1e-12); u=vr+mr
        return ShearTabResult(eccentricity,m,vr,mr,u,u<=1)
