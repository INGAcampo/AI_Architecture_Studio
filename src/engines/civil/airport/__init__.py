from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Runway:
    runway_id:str
    length:float
    width:float
    orientation_deg:float
class AirportLayoutEngine:
    def runway_area(self,r): return r.length*r.width
    def total_runway_area(self,runways): return sum(self.runway_area(r) for r in runways)
