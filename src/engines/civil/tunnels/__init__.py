from dataclasses import dataclass
from math import pi
@dataclass(frozen=True,slots=True)
class CircularTunnel:
    tunnel_id:str
    diameter:float
    length:float
class TunnelGeometryEngine:
    def excavation_area(self,t): return pi*t.diameter**2/4
    def excavation_volume(self,t): return self.excavation_area(t)*t.length
    def lining_area(self,t): return pi*t.diameter*t.length
