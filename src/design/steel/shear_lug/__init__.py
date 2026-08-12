from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ShearLugResult:
    bearing_capacity:float
    bending_capacity:float
    design_capacity:float
    ratio:float
    passed:bool

class ShearLugEngine:
    def calculate(self,width,depth,thickness,fy,fc,demand,phi=.9):
        bearing=.65*.85*fc*width*depth
        bending=phi*fy*width*thickness**2/(4*max(depth,1e-12))
        cap=min(bearing,bending)
        ratio=demand/max(cap,1e-12)
        return ShearLugResult(bearing,bending,cap,ratio,ratio<=1)
