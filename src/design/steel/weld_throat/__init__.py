from dataclasses import dataclass
from design.steel.weld_domain import WeldType
@dataclass(frozen=True,slots=True)
class WeldThroatResult: effective_throat:float; effective_length:float; effective_area:float
class EffectiveThroatEngine:
    def calculate(self,s):
        if s.size<=0 or s.length<=0: raise ValueError("Geometría inválida")
        t=.707*s.size if s.weld_type is WeldType.FILLET else (s.size if s.weld_type is WeldType.CJP else .75*s.size)
        return WeldThroatResult(t,s.length,t*s.length)
