from dataclasses import dataclass
from math import ceil

@dataclass(frozen=True, slots=True)
class StairType:
    type_id: str
    name: str
    target_riser: float
    tread_depth: float
    width: float

@dataclass(frozen=True, slots=True)
class StairInstance:
    stair_id: str
    stair_type: StairType
    base_elevation: float
    top_elevation: float

@dataclass(frozen=True, slots=True)
class StairGeometry:
    riser_count: int
    actual_riser: float
    tread_count: int
    run_length: float

class NativeBimStairEngine:
    def generate(self, stair):
        rise = stair.top_elevation - stair.base_elevation
        if rise <= 0:
            raise ValueError("Altura inválida")
        risers = ceil(rise / stair.stair_type.target_riser)
        actual = rise / risers
        treads = max(1, risers - 1)
        return StairGeometry(
            risers,
            actual,
            treads,
            treads * stair.stair_type.tread_depth,
        )

    def validate(self, stair):
        g = self.generate(stair)
        issues = []
        if not 0.10 <= g.actual_riser <= 0.20:
            issues.append("riser_out_of_range")
        if stair.stair_type.tread_depth < 0.25:
            issues.append("tread_too_shallow")
        return tuple(issues)
