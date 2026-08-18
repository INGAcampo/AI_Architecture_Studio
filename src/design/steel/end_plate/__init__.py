from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class EndPlateResult:
    plate_bending_ratio:float; bolt_tension_ratio:float; weld_ratio:float; unity_ratio:float; passed:bool
class EndPlateEngine:
    def design(self,plate_m,plate_cap,bolt_t,bolt_cap,weld,weld_cap):
        rs=(abs(plate_m)/plate_cap,abs(bolt_t)/bolt_cap,abs(weld)/weld_cap); u=max(rs)
        return EndPlateResult(*rs,u,u<=1)
