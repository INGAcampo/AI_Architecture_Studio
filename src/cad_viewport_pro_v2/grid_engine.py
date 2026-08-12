import math
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GridSpec:
    minor_spacing: float
    major_spacing: float
    major_every: int

class ProfessionalGridEngine:
    STEPS = (0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000)

    def spec(self, zoom: float, target_pixels: float = 32.0, major_every: int = 5) -> GridSpec:
        target = target_pixels / max(zoom, 1e-9)
        minor = min(self.STEPS, key=lambda step: abs(math.log10(max(step/target, 1e-12))))
        return GridSpec(minor, minor * max(2, major_every), max(2, major_every))
