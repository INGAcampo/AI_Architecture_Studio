from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ClipAngleResult:
    leg_bending_ratio:float; bolt_ratio:float; angle_shear_ratio:float; unity_ratio:float; passed:bool
class ClipAngleEngine:
    def design(self,leg_moment,leg_capacity,bolt_demand,bolt_capacity,shear,shear_capacity):
        a=abs(leg_moment)/max(leg_capacity,1e-12); b=abs(bolt_demand)/max(bolt_capacity,1e-12); c=abs(shear)/max(shear_capacity,1e-12); u=max(a,b,c)
        return ClipAngleResult(a,b,c,u,u<=1)
