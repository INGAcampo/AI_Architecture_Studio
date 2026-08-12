from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class BearingPressureResult:
    area:float
    average_pressure:float
    maximum_pressure:float
    minimum_pressure:float
    full_contact:bool

class BearingPressureEngine:
    def calculate(self,plate,demand):
        area=plate.width*plate.length
        avg=demand.axial/max(area,1e-12)
        sx=plate.width*plate.length**2/6
        sy=plate.length*plate.width**2/6
        qx=abs(demand.moment_x)/max(sx,1e-12)
        qy=abs(demand.moment_y)/max(sy,1e-12)
        qmax=avg+qx+qy
        qmin=avg-qx-qy
        return BearingPressureResult(area,avg,qmax,qmin,qmin>=0)
