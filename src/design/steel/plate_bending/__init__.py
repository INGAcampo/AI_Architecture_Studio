from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True,slots=True)
class PlateBendingResult:
    projection_x:float
    projection_y:float
    governing_projection:float
    required_thickness:float
    provided_thickness:float
    ratio:float
    passed:bool

class PlateBendingEngine:
    def calculate(self,plate,column,pressure,phi=.9):
        nx=max((plate.width-column.width)/2,0)
        ny=max((plate.length-column.depth)/2,0)
        m=max(nx,ny)
        required=m*sqrt(max(2*pressure/(phi*plate.fy),0))
        ratio=required/max(plate.thickness,1e-12)
        return PlateBendingResult(nx,ny,m,required,plate.thickness,ratio,ratio<=1)
