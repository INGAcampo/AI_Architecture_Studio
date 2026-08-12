from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Junction:
    junction_id: str
    connected_alignment_ids: tuple[str, ...]
    radius: float

class ParametricIntersectionNetwork:
    def degree(self, junction):
        return len(junction.connected_alignment_ids)

    def is_valid(self, junction):
        return self.degree(junction) >= 2 and junction.radius > 0
