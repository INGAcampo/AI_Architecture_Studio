from dataclasses import dataclass
from math import pi
@dataclass(frozen=True,slots=True)
class CircularCulvert:
    culvert_id:str
    diameter:float
    slope:float
    roughness_n:float
class CulvertDesignEngine:
    def area(self,c): return pi*c.diameter**2/4
    def hydraulic_radius(self,c): return c.diameter/4
    def capacity(self,c): return (1/c.roughness_n)*self.area(c)*self.hydraulic_radius(c)**(2/3)*c.slope**0.5
