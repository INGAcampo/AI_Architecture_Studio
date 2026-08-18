from dataclasses import dataclass
from enum import Enum
class TransportMode(str,Enum):
    ROAD="road";RAIL="rail";BIKE="bike";PEDESTRIAN="pedestrian"
@dataclass(frozen=True,slots=True)
class CorridorMode:
    mode:TransportMode
    width:float
class MultimodalCorridorEngine:
    def total_width(self,modes): return sum(m.width for m in modes)
    def modal_share(self,modes,mode):
        total=self.total_width(modes)
        return sum(m.width for m in modes if m.mode is mode)/total
