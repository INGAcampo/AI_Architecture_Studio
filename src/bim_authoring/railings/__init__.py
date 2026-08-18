from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class RailingType:
    type_id: str
    name: str
    height: float
    post_spacing: float
    material_id: str

@dataclass(frozen=True, slots=True)
class RailingInstance:
    railing_id: str
    railing_type: RailingType
    path: tuple[tuple[float,float,float], ...]

@dataclass(frozen=True, slots=True)
class RailingQuantities:
    path_length: float
    post_count: int

class NativeBimRailingEngine:
    def quantities(self, railing):
        length = sum(
            hypot(
                railing.path[i+1][0]-railing.path[i][0],
                railing.path[i+1][1]-railing.path[i][1],
            )
            for i in range(len(railing.path)-1)
        )
        posts = int(length / railing.railing_type.post_spacing) + 1
        return RailingQuantities(length, posts)

    def validate(self, railing):
        issues = []
        if railing.railing_type.height < 0.90:
            issues.append("railing_too_low")
        if railing.railing_type.post_spacing > 1.5:
            issues.append("post_spacing_too_large")
        return tuple(issues)
