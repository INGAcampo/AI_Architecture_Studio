from dataclasses import dataclass
from enum import Enum

class EnergyCarrier(str, Enum):
    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    DISTRICT_HEATING = "district_heating"
    DISTRICT_COOLING = "district_cooling"
    RENEWABLE = "renewable"

@dataclass(frozen=True, slots=True)
class EnergyUse:
    use_id: str
    carrier: EnergyCarrier
    annual_kwh: float
    floor_area_m2: float

    def __post_init__(self):
        if not self.use_id.strip() or self.annual_kwh < 0 or self.floor_area_m2 <= 0:
            raise ValueError("Datos energéticos inválidos")

    @property
    def intensity(self):
        return self.annual_kwh / self.floor_area_m2

class EnergyAnalysisFoundation:
    def total_energy(self, uses):
        return sum(use.annual_kwh for use in uses)

    def energy_use_intensity(self, uses):
        total_area = sum(use.floor_area_m2 for use in uses)
        if total_area <= 0:
            raise ValueError("Área total inválida")
        return self.total_energy(uses) / total_area

    def by_carrier(self, uses, carrier):
        return tuple(use for use in uses if use.carrier is carrier)
