from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class IntersectionArm:
    arm_id:str
    approach_width:float
    departure_width:float
    angle_deg:float
    def __post_init__(self):
        if not self.arm_id.strip() or min(self.approach_width,self.departure_width)<=0: raise ValueError("Datos inválidos")
class IntersectionGeometryEngine:
    def total_paved_width(self,arms): return sum(a.approach_width+a.departure_width for a in arms)
    def average_angle(self,arms):
        arms=tuple(arms); return sum(a.angle_deg for a in arms)/len(arms)
