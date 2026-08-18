from dataclasses import dataclass
from math import cos, radians

@dataclass(frozen=True, slots=True)
class EnergyVariant:
    variant_id: str
    orientation_deg: float
    window_ratio: float
    insulation_r: float
    shading_factor: float

@dataclass(frozen=True, slots=True)
class EnergyScore:
    variant_id: str
    heating: float
    cooling: float
    daylight: float
    total_energy: float

class EnergyOptimizationEngine:
    def evaluate(self, variant, *, climate_factor=1.0):
        solar = max(0.0, cos(radians(variant.orientation_deg - 180)))
        heating = climate_factor * 100 / max(variant.insulation_r, 0.1)
        cooling = climate_factor * (40 * variant.window_ratio * (1 + solar) * variant.shading_factor)
        daylight = 100 * variant.window_ratio * (0.5 + 0.5 * solar)
        return EnergyScore(
            variant.variant_id,
            heating,
            cooling,
            daylight,
            heating + cooling,
        )

    def select_minimum_energy(self, variants, *, climate_factor=1.0):
        scores = tuple(self.evaluate(v, climate_factor=climate_factor) for v in variants)
        return min(scores, key=lambda score: score.total_energy)
