from dataclasses import dataclass
from enum import Enum

class CarbonScope(str, Enum):
    EMBODIED = "embodied"
    OPERATIONAL = "operational"
    TRANSPORT = "transport"
    END_OF_LIFE = "end_of_life"

@dataclass(frozen=True, slots=True)
class CarbonItem:
    item_id: str
    scope: CarbonScope
    quantity: float
    emission_factor: float

    def __post_init__(self):
        if not self.item_id.strip() or self.quantity < 0 or self.emission_factor < 0:
            raise ValueError("Datos inválidos")

    @property
    def emissions(self):
        return self.quantity * self.emission_factor

class SustainabilityCarbonEngine:
    def total_emissions(self, items):
        return sum(item.emissions for item in items)

    def by_scope(self, items, scope):
        return tuple(item for item in items if item.scope is scope)

    def carbon_intensity(self, items, floor_area):
        if floor_area <= 0:
            raise ValueError("Área inválida")
        return self.total_emissions(items) / floor_area
