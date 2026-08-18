from dataclasses import dataclass
from math import cos, radians

@dataclass(frozen=True, slots=True)
class SolarSurface:
    surface_id: str
    area: float
    irradiance: float
    incidence_angle_deg: float
    shading_factor: float = 1.0
    def __post_init__(self):
        if not self.surface_id.strip() or self.area <= 0 or self.irradiance < 0:
            raise ValueError("Datos inválidos")
        if not 0 <= self.shading_factor <= 1:
            raise ValueError("shading_factor inválido")

class SolarExposureEngine:
    def incident_energy(self, surface):
        projected = max(cos(radians(surface.incidence_angle_deg)), 0.0)
        return surface.area * surface.irradiance * projected * surface.shading_factor
