from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EarthworkCell:
    cell_id: str
    area: float
    existing_elevation: float
    proposed_elevation: float

    def __post_init__(self):
        if not self.cell_id.strip() or self.area <= 0:
            raise ValueError("Datos inválidos")

    @property
    def depth(self):
        return self.proposed_elevation - self.existing_elevation

class EarthworkEngine:
    def cut_volume(self, cells):
        return sum(
            abs(cell.depth) * cell.area
            for cell in cells
            if cell.depth < 0
        )

    def fill_volume(self, cells):
        return sum(
            cell.depth * cell.area
            for cell in cells
            if cell.depth > 0
        )

    def net_volume(self, cells):
        return self.fill_volume(cells) - self.cut_volume(cells)
