from dataclasses import dataclass
from enum import Enum
class ClashKind(str,Enum): HARD="hard";CLEARANCE="clearance";DUPLICATE="duplicate"
@dataclass(frozen=True,slots=True)
class BoundingBox:
    min_x:float;min_y:float;min_z:float;max_x:float;max_y:float;max_z:float
    def __post_init__(self):
        if self.min_x>self.max_x or self.min_y>self.max_y or self.min_z>self.max_z:raise ValueError("BoundingBox inválido")
@dataclass(frozen=True,slots=True)
class Clash:
    first_id:str;second_id:str;kind:ClashKind
class ClashDetector:
    def intersects(self,a,b,clearance=0.0):
        return not (a.max_x+clearance<b.min_x or b.max_x+clearance<a.min_x or a.max_y+clearance<b.min_y or b.max_y+clearance<a.min_y or a.max_z+clearance<b.min_z or b.max_z+clearance<a.min_z)
    def detect(self,first_id,first_box,second_id,second_box):
        return Clash(first_id,second_id,ClashKind.HARD) if self.intersects(first_box,second_box) else None
