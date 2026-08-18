from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnSpliceResult:
    axial_ratio:float; moment_ratio:float; shear_ratio:float; unity_ratio:float; passed:bool
class ColumnSpliceEngine:
    def design(self,axial,axial_cap,moment,moment_cap,shear,shear_cap):
        rs=(abs(axial)/axial_cap,abs(moment)/moment_cap,abs(shear)/shear_cap); u=max(rs)
        return ColumnSpliceResult(*rs,u,u<=1)
