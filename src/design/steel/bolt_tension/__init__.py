from dataclasses import dataclass
from design.steel.bolt_area import BoltAreaEngine

@dataclass(frozen=True, slots=True)
class BoltTensionResult:
    nominal_capacity:float
    design_capacity:float

class BoltTensionEngine:
    def __init__(self): self.area=BoltAreaEngine()
    def calculate(self,bolt,phi=0.75):
        area=self.area.calculate(bolt).tensile_area
        nominal=bolt.material.nominal_tensile_strength*area
        return BoltTensionResult(nominal,phi*nominal)
