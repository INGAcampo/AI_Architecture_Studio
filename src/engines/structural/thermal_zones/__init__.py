from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EnvelopeSurface:
    surface_id: str
    area: float
    u_value: float
    interior_temperature: float
    exterior_temperature: float

    def __post_init__(self):
        if not self.surface_id.strip() or self.area <= 0 or self.u_value < 0:
            raise ValueError("Datos inválidos")

    @property
    def heat_transfer(self):
        return self.area * self.u_value * (
            self.interior_temperature - self.exterior_temperature
        )

@dataclass(frozen=True, slots=True)
class ThermalZone:
    zone_id: str
    name: str
    volume: float
    surfaces: tuple[EnvelopeSurface, ...]

    def __post_init__(self):
        if not self.zone_id.strip() or not self.name.strip() or self.volume <= 0:
            raise ValueError("Datos inválidos")

class ThermalZoneEngine:
    def transmission_load(self, zone):
        return sum(surface.heat_transfer for surface in zone.surfaces)

    def air_change_load(self, zone, air_changes_per_hour, density=1.2, heat_capacity=1005):
        if air_changes_per_hour < 0:
            raise ValueError("ACH inválido")
        mass_flow = zone.volume * air_changes_per_hour * density / 3600
        return mass_flow * heat_capacity
