from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ExtendedEndPlateResult:
    bolt_row_force:float; plate_ratio:float; bolt_ratio:float; panel_zone_ratio:float; unity_ratio:float; passed:bool
class ExtendedEndPlateEngine:
    def design(self,moment,lever_arm,plate_cap,bolt_cap,panel_zone_cap):
        force=abs(moment)/max(lever_arm,1e-12); rs=(force/plate_cap,force/bolt_cap,abs(moment)/panel_zone_cap); u=max(rs)
        return ExtendedEndPlateResult(force,*rs,u,u<=1)
