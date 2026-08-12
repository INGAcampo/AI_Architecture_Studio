from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class FoundationQuantities:
    plan_area: float
    concrete_volume: float
    excavation_volume: float
    mass: float
    weight: float
    contact_pressure: float | None
class FoundationQuantityCalculator:
    GRAVITY = 9.80665
    def calculate(self, foundation, material, applied_load=None, excavation_allowance=0.20):
        volume = foundation.volume
        mass = volume * material.density
        pressure = None if applied_load is None else applied_load / foundation.plan_area
        return FoundationQuantities(
            foundation.plan_area, volume,
            (foundation.length+2*excavation_allowance)*(foundation.width+2*excavation_allowance)*(foundation.depth+excavation_allowance),
            mass, mass*self.GRAVITY, pressure
        )
