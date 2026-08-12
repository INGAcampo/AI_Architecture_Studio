from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SlipCriticalResult:
    nominal_capacity:float
    design_capacity:float
    slip_coefficient:float
    faying_surfaces:int

class SlipCriticalEngine:
    def calculate(self,pretension,slip_coefficient=0.30,faying_surfaces=1,hole_factor=1.0,phi=1.0):
        nominal=pretension*slip_coefficient*faying_surfaces*hole_factor
        return SlipCriticalResult(nominal,phi*nominal,slip_coefficient,faying_surfaces)
