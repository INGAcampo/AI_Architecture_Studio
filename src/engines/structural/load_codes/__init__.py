from dataclasses import dataclass
from enum import Enum

class LoadCode(str, Enum):
    ASCE7="ASCE 7"
    EUROCODE="EN 1991"
    COVENIN="COVENIN"
    NSR="NSR"
    CTE="CTE"

@dataclass(frozen=True, slots=True)
class WindParameters:
    basic_speed: float
    exposure_factor: float = 1.0
    importance_factor: float = 1.0
    def __post_init__(self):
        if min(self.basic_speed, self.exposure_factor, self.importance_factor) <= 0:
            raise ValueError("Parámetros inválidos")

class LoadCodeEngine:
    AIR_DENSITY = 1.225
    def wind_pressure(self, parameters):
        return 0.5 * self.AIR_DENSITY * parameters.basic_speed**2 * parameters.exposure_factor * parameters.importance_factor
    def seismic_base_shear(self, weight, coefficient):
        if weight <= 0 or coefficient < 0:
            raise ValueError("Datos inválidos")
        return weight * coefficient
