from dataclasses import dataclass
from math import pi

@dataclass(frozen=True, slots=True)
class BoltAreaResult:
    gross_area:float
    tensile_area:float
    shear_area:float

class BoltAreaEngine:
    def calculate(self,bolt):
        gross=pi*bolt.diameter**2/4.0
        tensile=0.78*gross
        shear=tensile if bolt.threads_in_shear_plane else gross
        return BoltAreaResult(gross,tensile,shear)
