from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnWebCheckResult:
    yielding_ratio:float; crippling_ratio:float; buckling_ratio:float; unity_ratio:float; passed:bool
class ColumnWebCheckEngine:
    def design(self,force,yield_cap,crippling_cap,buckling_cap):
        rs=(abs(force)/yield_cap,abs(force)/crippling_cap,abs(force)/buckling_cap); u=max(rs)
        return ColumnWebCheckResult(*rs,u,u<=1)
