from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CeilingType:
    type_id: str
    name: str
    thickness: float
    material_id: str

@dataclass(frozen=True, slots=True)
class CeilingInstance:
    ceiling_id: str
    ceiling_type: CeilingType
    boundary: tuple[tuple[float,float], ...]
    elevation: float
    room_id: str | None = None

class NativeBimCeilingEngine:
    def area(self, ceiling):
        p = ceiling.boundary
        return abs(sum(
            p[i][0]*p[(i+1)%len(p)][1] -
            p[(i+1)%len(p)][0]*p[i][1]
            for i in range(len(p))
        )) / 2

    def volume(self, ceiling):
        return self.area(ceiling) * ceiling.ceiling_type.thickness

    def validate(self, ceiling):
        issues = []
        if len(ceiling.boundary) < 3:
            issues.append("invalid_boundary")
        if ceiling.ceiling_type.thickness <= 0:
            issues.append("invalid_thickness")
        return tuple(issues)
