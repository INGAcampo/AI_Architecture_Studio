from dataclasses import dataclass
from design.steel.weld_domain import WeldType
from design.steel.weld_throat import EffectiveThroatEngine
@dataclass(frozen=True,slots=True)
class GrooveWeldResult: nominal_capacity:float; design_capacity:float; penetration_factor:float
class GrooveWeldEngine:
    def calculate(self,s,base_strength,phi=.9):
        if s.weld_type not in {WeldType.CJP,WeldType.PJP}: raise ValueError("Tipo inválido")
        g=EffectiveThroatEngine().calculate(s); f=1. if s.weld_type is WeldType.CJP else .75
        n=min(s.material.tensile_strength,base_strength)*g.effective_area*f
        return GrooveWeldResult(n,phi*n,f)
