from dataclasses import dataclass
from enum import Enum

class CertificationSystem(str, Enum):
    LEED="LEED"
    BREEAM="BREEAM"
    EDGE="EDGE"
    WELL="WELL"

@dataclass(frozen=True, slots=True)
class CertificationCredit:
    credit_id: str
    points_earned: float
    points_available: float
    def __post_init__(self):
        if not self.credit_id.strip() or self.points_earned < 0 or self.points_available <= 0:
            raise ValueError("Datos inválidos")

class CertificationDashboard:
    def score(self, credits):
        credits = tuple(credits)
        return sum(c.points_earned for c in credits) / sum(c.points_available for c in credits) * 100
