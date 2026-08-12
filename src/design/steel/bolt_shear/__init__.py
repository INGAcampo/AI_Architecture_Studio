from dataclasses import dataclass
from design.steel.bolt_area import BoltAreaEngine

@dataclass(frozen=True, slots=True)
class BoltShearResult:
    nominal_capacity:float
    design_capacity:float
    planes:int

class BoltShearEngine:
    def __init__(self): self.area=BoltAreaEngine()
    def calculate(self,bolt,shear_planes=1,phi=0.75):
        if shear_planes<1: raise ValueError("Número de planos inválido")
        area=self.area.calculate(bolt).shear_area
        nominal=bolt.material.nominal_shear_strength*area*shear_planes
        return BoltShearResult(nominal,phi*nominal,shear_planes)
