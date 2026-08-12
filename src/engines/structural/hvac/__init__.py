from dataclasses import dataclass
from enum import Enum

class HvacSystemType(str, Enum):
    SPLIT = "split"
    VRF = "vrf"
    CHILLED_WATER = "chilled_water"
    HEAT_PUMP = "heat_pump"
    NATURAL_VENTILATION = "natural_ventilation"

@dataclass(frozen=True, slots=True)
class HvacSystem:
    system_id: str
    system_type: HvacSystemType
    capacity_kw: float
    efficiency: float

    def __post_init__(self):
        if not self.system_id.strip() or self.capacity_kw <= 0 or self.efficiency <= 0:
            raise ValueError("Datos HVAC inválidos")

class HvacSystemEngine:
    def electrical_power(self, system, thermal_load_kw):
        if thermal_load_kw < 0:
            raise ValueError("Carga inválida")
        return thermal_load_kw / system.efficiency

    def utilization(self, system, thermal_load_kw):
        return thermal_load_kw / system.capacity_kw

    def is_adequate(self, system, thermal_load_kw, max_utilization=1.0):
        return self.utilization(system, thermal_load_kw) <= max_utilization
