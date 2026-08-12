from dataclasses import dataclass
from design.steel.bearing_pressure import BearingPressureEngine
from design.steel.concrete_bearing import ConcreteBearingEngine
from design.steel.plate_bending import PlateBendingEngine
from design.steel.anchor_rod_strength import AnchorRodStrengthEngine
from design.steel.anchor_group import AnchorGroupEngine
from design.steel.anchor_interaction import AnchorInteractionEngine

@dataclass(frozen=True,slots=True)
class BasePlateDesignResult:
    bearing:object
    concrete:object
    plate_bending:object
    anchor_forces:tuple
    anchor_checks:tuple
    maximum_unity:float
    passed:bool
    governing_check:str

class BasePlateDesignEngine:
    def design(self,plate,column,anchors,demand,fc,supporting_area):
        bearing=BearingPressureEngine().calculate(plate,demand)
        concrete=ConcreteBearingEngine().calculate(fc,bearing.area,supporting_area,demand.axial)
        bending=PlateBendingEngine().calculate(plate,column,bearing.maximum_pressure)
        forces=AnchorGroupEngine().distribute(anchors,demand)
        checks=[]
        by={a.anchor_id:a for a in anchors}
        for f in forces:
            s=AnchorRodStrengthEngine().calculate(by[f.anchor_id])
            checks.append(AnchorInteractionEngine().calculate(f.tension,s.tension_capacity,f.shear,s.shear_capacity))
        values={"concrete":concrete.ratio,"plate":bending.ratio,"anchors":max((c.interaction_ratio for c in checks),default=0)}
        gov=max(values,key=values.get); mx=values[gov]
        return BasePlateDesignResult(bearing,concrete,bending,forces,tuple(checks),mx,mx<=1,gov)
