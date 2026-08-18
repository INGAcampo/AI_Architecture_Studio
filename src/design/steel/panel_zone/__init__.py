from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PanelZoneResult:
    shear_demand:float; shear_capacity:float; ratio:float; passed:bool
class PanelZoneEngine:
    def design(self,moment_left,moment_right,story_shear,depth,capacity):
        demand=abs(moment_left+moment_right)/max(depth,1e-12)+abs(story_shear)
        r=demand/max(capacity,1e-12)
        return PanelZoneResult(demand,capacity,r,r<=1)
