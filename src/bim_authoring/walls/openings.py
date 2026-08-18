from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WallOpening:
    opening_id: str
    wall_id: str
    offset: float
    width: float
    sill_height: float
    height: float
    hosted_element_id: str | None = None

    def __post_init__(self):
        if not self.opening_id.strip() or not self.wall_id.strip():
            raise ValueError("IDs obligatorios")
        if self.offset < 0 or self.width <= 0 or self.height <= 0 or self.sill_height < 0:
            raise ValueError("Geometría de abertura inválida")

class WallOpeningManager:
    def __init__(self):
        self._openings = {}

    def add(self, wall, opening):
        if opening.wall_id != wall.wall_id:
            raise ValueError("La abertura no pertenece al muro")
        if opening.offset + opening.width > wall.profile.length:
            raise ValueError("La abertura excede la longitud del muro")
        if opening.sill_height + opening.height > wall.profile.height:
            raise ValueError("La abertura excede la altura del muro")
        self._openings[opening.opening_id] = opening
        return opening

    def for_wall(self, wall_id):
        return tuple(
            opening for opening in self._openings.values()
            if opening.wall_id == wall_id
        )

    def remove(self, opening_id):
        return self._openings.pop(opening_id)
