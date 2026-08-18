from dataclasses import dataclass
from math import pi

@dataclass(frozen=True, slots=True)
class WaterPipe:
    pipe_id: str
    length: float
    diameter: float
    roughness: float
    flow_rate: float

    def __post_init__(self):
        if not self.pipe_id.strip() or min(
            self.length, self.diameter, self.roughness, self.flow_rate
        ) <= 0:
            raise ValueError("Datos inválidos")

    @property
    def area(self):
        return pi * self.diameter**2 / 4

    @property
    def velocity(self):
        return self.flow_rate / self.area

class WaterDistributionEngine:
    def head_loss_hazen_williams(self, pipe):
        c = pipe.roughness
        return 10.67 * pipe.length * pipe.flow_rate**1.852 / (
            c**1.852 * pipe.diameter**4.87
        )

    def pressure_drop(self, pipe, density=1000.0, gravity=9.81):
        return density * gravity * self.head_loss_hazen_williams(pipe)
