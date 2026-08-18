from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnFlangeCheckResult:
    bending_ratio:float; local_yield_ratio:float; crippling_ratio:float; unity_ratio:float; passed:bool
class ColumnFlangeCheckEngine:
    def design(self,force,bending_cap,yield_cap,crippling_cap):
        rs=(abs(force)/bending_cap,abs(force)/yield_cap,abs(force)/crippling_cap); u=max(rs)
        return ColumnFlangeCheckResult(*rs,u,u<=1)
