from dataclasses import dataclass
from design.steel.weld_throat import EffectiveThroatEngine
@dataclass(frozen=True,slots=True)
class FilletWeldStrengthResult: nominal_capacity:float; design_capacity:float; effective_area:float
class FilletWeldStrengthEngine:
    def calculate(self,s,phi=.75):
        g=EffectiveThroatEngine().calculate(s); n=.60*s.material.tensile_strength*g.effective_area
        return FilletWeldStrengthResult(n,phi*n,g.effective_area)
