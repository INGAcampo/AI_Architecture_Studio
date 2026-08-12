from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class BraceGussetResult:
    yielding_ratio:float; buckling_ratio:float; block_shear_ratio:float; unity_ratio:float; passed:bool
class BraceGussetEngine:
    def design(self,demand,yield_cap,buckling_cap,block_cap):
        rs=(abs(demand)/yield_cap,abs(demand)/buckling_cap,abs(demand)/block_cap); u=max(rs)
        return BraceGussetResult(*rs,u,u<=1)
