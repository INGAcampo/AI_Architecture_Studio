from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CorridorSection:
    station: float
    left_width: float
    right_width: float
    elevation: float

    def __post_init__(self):
        if self.station < 0 or self.left_width < 0 or self.right_width < 0:
            raise ValueError("Datos inválidos")

class CorridorModel:
    def __init__(self, corridor_id, sections):
        if not corridor_id.strip():
            raise ValueError("corridor_id obligatorio")
        self.corridor_id = corridor_id
        self.sections = tuple(sorted(sections, key=lambda s: s.station))
        if len(self.sections) < 2:
            raise ValueError("Se requieren al menos dos secciones")

    def width_at(self, station):
        nearest = min(self.sections, key=lambda s: abs(s.station-station))
        return nearest.left_width + nearest.right_width

    def elevation_range(self):
        values = [s.elevation for s in self.sections]
        return min(values), max(values)
