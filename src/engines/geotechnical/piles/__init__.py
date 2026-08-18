from dataclasses import dataclass
from math import pi
@dataclass(frozen=True,slots=True)
class Pile:
    pile_id:str; diameter:float; length:float; tip_resistance:float; shaft_resistance:float
    @property
    def base_area(self): return pi*self.diameter**2/4
    @property
    def shaft_area(self): return pi*self.diameter*self.length
class PileFoundationEngine:
    def ultimate_capacity(self,p): return p.tip_resistance*p.base_area+p.shaft_resistance*p.shaft_area
    def allowable_capacity(self,p,fs=2.5): return self.ultimate_capacity(p)/fs
