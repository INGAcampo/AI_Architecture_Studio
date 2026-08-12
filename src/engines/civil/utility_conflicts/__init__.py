from dataclasses import dataclass
from math import dist

@dataclass(frozen=True, slots=True)
class UtilityPoint:
    utility_id: str
    x: float
    y: float
    z: float
    clearance: float

class UtilityConflictResolver:
    def conflicts(self, a, b):
        return dist((a.x,a.y,a.z),(b.x,b.y,b.z)) < (a.clearance+b.clearance)

    def required_separation(self, a, b):
        return a.clearance+b.clearance
