from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DoublerPlateResult:
    excess_shear:float; plate_capacity:float; ratio:float; required:bool; passed:bool
class DoublerPlateEngine:
    def design(self,panel_demand,panel_capacity,plate_capacity):
        excess=max(0,panel_demand-panel_capacity); r=excess/max(plate_capacity,1e-12)
        return DoublerPlateResult(excess,plate_capacity,r,excess>0,r<=1)
