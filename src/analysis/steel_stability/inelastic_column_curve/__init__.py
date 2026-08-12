from __future__ import annotations
import math
from dataclasses import dataclass

MODULE_NAME = 'inelastic_column_curve'

@dataclass(frozen=True, slots=True)
class StabilityCheck:
    value: float
    limit: float
    status: str

class StabilityEngine:
    def euler_load(self, e_mpa: float, i_mm4: float, k: float, length_mm: float) -> float:
        return math.pi**2 * e_mpa * i_mm4 / max((k*length_mm)**2, 1e-12)

    def slenderness(self, k: float, length_mm: float, radius_mm: float) -> float:
        return k*length_mm/max(radius_mm,1e-12)

    def p_delta_factor(self, theta: float) -> float:
        return 1.0/max(1.0-theta,1e-6)

    def notional_load(self, gravity_n: float, coefficient: float=0.002) -> float:
        return gravity_n*coefficient

    def check(self, demand: float, capacity: float) -> StabilityCheck:
        unity=abs(demand)/max(abs(capacity),1e-12)
        return StabilityCheck(unity,1.0,'PASS' if unity<=1.0 else 'FAIL')
