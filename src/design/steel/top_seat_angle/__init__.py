from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class TopSeatAngleResult:
    shear_ratio:float; moment_ratio:float; prying_ratio:float; unity_ratio:float; passed:bool
class TopSeatAngleEngine:
    def design(self,shear,shear_cap,moment,moment_cap,prying,prying_cap):
        rs=(abs(shear)/shear_cap,abs(moment)/moment_cap,abs(prying)/prying_cap); u=max(rs)
        return TopSeatAngleResult(*rs,u,u<=1)
