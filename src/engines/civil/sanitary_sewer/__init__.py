from dataclasses import dataclass
from math import pi

@dataclass(frozen=True, slots=True)
class SewerPipe:
    pipe_id: str
    diameter: float
    slope: float
    roughness_n: float
    fill_ratio: float = 1.0

    def __post_init__(self):
        if not self.pipe_id.strip() or min(
            self.diameter, self.slope, self.roughness_n
        ) <= 0:
            raise ValueError("Datos inválidos")
        if not 0 < self.fill_ratio <= 1:
            raise ValueError("fill_ratio inválido")

class SanitarySewerEngine:
    def full_flow_area(self, pipe):
        return pi * pipe.diameter**2 / 4

    def hydraulic_radius(self, pipe):
        return pipe.diameter / 4

    def capacity_manning(self, pipe):
        area = self.full_flow_area(pipe) * pipe.fill_ratio
        radius = self.hydraulic_radius(pipe)
        return (
            (1 / pipe.roughness_n)
            * area
            * radius**(2/3)
            * pipe.slope**0.5
        )
