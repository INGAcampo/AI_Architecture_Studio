from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True,slots=True)
class ConcreteBearingResult:
    nominal_capacity:float
    design_capacity:float
    confinement_factor:float
    ratio:float
    passed:bool

class ConcreteBearingEngine:
    def calculate(self,fc,loaded_area,supporting_area,demand,phi=.65):
        factor=min(2.0,sqrt(max(supporting_area,loaded_area)/max(loaded_area,1e-12)))
        nominal=.85*fc*loaded_area*factor
        design=phi*nominal
        ratio=demand/max(design,1e-12)
        return ConcreteBearingResult(nominal,design,factor,ratio,ratio<=1)
