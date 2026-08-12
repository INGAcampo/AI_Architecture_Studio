from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DaylightSensor:
    sensor_id: str
    illuminance_lux: float
    target_lux: float
    def __post_init__(self):
        if not self.sensor_id.strip() or self.illuminance_lux < 0 or self.target_lux <= 0:
            raise ValueError("Datos inválidos")
    @property
    def compliance_ratio(self):
        return self.illuminance_lux / self.target_lux

class DaylightingEngine:
    def average_illuminance(self, sensors):
        sensors = tuple(sensors)
        return sum(s.illuminance_lux for s in sensors) / len(sensors)
    def compliant_count(self, sensors):
        return sum(sensor.illuminance_lux >= sensor.target_lux for sensor in sensors)
