from dataclasses import dataclass
from enum import Enum

class SteelDesignMethod(str, Enum):
    LRFD="lrfd"
    ASD="asd"

@dataclass(frozen=True, slots=True)
class SteelSectionCapacity:
    section_id: str
    axial_capacity: float
    moment_capacity: float
    shear_capacity: float
    def __post_init__(self):
        if not self.section_id.strip() or min(self.axial_capacity, self.moment_capacity, self.shear_capacity) <= 0:
            raise ValueError("Capacidades inválidas")

class SteelDesignEngine:
    def demand_capacity_ratio(self, demand, capacity):
        if capacity <= 0:
            raise ValueError("capacity debe ser positiva")
        return abs(demand) / capacity
    def interaction_ratio(self, axial_demand, moment_demand, capacity):
        return (
            self.demand_capacity_ratio(axial_demand, capacity.axial_capacity)
            + self.demand_capacity_ratio(moment_demand, capacity.moment_capacity)
        )
    def passes(self, ratio, limit=1.0):
        return ratio <= limit
