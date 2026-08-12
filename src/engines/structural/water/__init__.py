from dataclasses import dataclass
from enum import Enum

class WaterUseType(str, Enum):
    DOMESTIC="domestic"
    IRRIGATION="irrigation"
    PROCESS="process"
    FIRE="fire"

@dataclass(frozen=True, slots=True)
class WaterUse:
    use_id: str
    use_type: WaterUseType
    daily_liters: float
    occupants: int = 1
    def __post_init__(self):
        if not self.use_id.strip() or self.daily_liters < 0 or self.occupants < 1:
            raise ValueError("Datos inválidos")

class WaterConsumptionEngine:
    def annual_liters(self, uses):
        return sum(use.daily_liters for use in uses) * 365
    def liters_per_person_day(self, uses):
        uses = tuple(uses)
        return sum(use.daily_liters for use in uses) / sum(use.occupants for use in uses)
