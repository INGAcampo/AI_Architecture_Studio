from dataclasses import dataclass
from math import tan, radians

@dataclass(frozen=True, slots=True)
class SlopeSlice:
    slice_id: str
    normal_force: float
    driving_force: float
    cohesion_force: float
    friction_angle_deg: float

class SlopeStabilityEngine:
    def factor_of_safety(self, slices):
        resisting = sum(
            s.cohesion_force + s.normal_force * tan(radians(s.friction_angle_deg))
            for s in slices
        )
        driving = sum(s.driving_force for s in slices)
        if driving <= 0:
            raise ValueError("Fuerza motriz inválida")
        return resisting / driving
