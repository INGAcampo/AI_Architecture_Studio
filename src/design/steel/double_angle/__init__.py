from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DoubleAngleResult:
    per_angle_shear:float; angle_ratio:float; bolt_ratio:float; unity_ratio:float; passed:bool
class DoubleAngleEngine:
    def design(self,total_shear,angle_capacity_each,bolt_capacity_total):
        per=total_shear/2; ar=abs(per)/max(angle_capacity_each,1e-12); br=abs(total_shear)/max(bolt_capacity_total,1e-12); u=max(ar,br)
        return DoubleAngleResult(per,ar,br,u,u<=1)
