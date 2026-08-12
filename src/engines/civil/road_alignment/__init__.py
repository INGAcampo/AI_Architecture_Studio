from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class AlignmentPoint:
    point_id: str
    x: float
    y: float
    elevation: float = 0.0

    def __post_init__(self):
        if not self.point_id.strip():
            raise ValueError("point_id obligatorio")

@dataclass(frozen=True, slots=True)
class RoadAlignment:
    alignment_id: str
    points: tuple[AlignmentPoint, ...]

    def __post_init__(self):
        if not self.alignment_id.strip() or len(self.points) < 2:
            raise ValueError("Alineamiento inválido")

class RoadAlignmentEngine:
    def segment_lengths(self, alignment):
        return tuple(
            hypot(b.x-a.x, b.y-a.y)
            for a, b in zip(alignment.points, alignment.points[1:])
        )

    def total_length(self, alignment):
        return sum(self.segment_lengths(alignment))

    def station_of_point(self, alignment, point_index):
        if point_index < 0 or point_index >= len(alignment.points):
            raise IndexError(point_index)
        return sum(self.segment_lengths(alignment)[:point_index])
