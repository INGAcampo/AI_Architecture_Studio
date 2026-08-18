from dataclasses import dataclass
from math import pi

@dataclass(frozen=True,slots=True)
class AnchorRodStrengthResult:
    area:float
    tension_capacity:float
    shear_capacity:float

class AnchorRodStrengthEngine:
    def calculate(self,anchor,phi_t=.75,phi_v=.75):
        area=pi*anchor.diameter**2/4
        return AnchorRodStrengthResult(area,phi_t*.75*anchor.fu*area,phi_v*.45*anchor.fu*area)
