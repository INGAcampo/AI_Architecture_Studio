from __future__ import annotations

from dataclasses import dataclass

from .geometry import point_in_polygon, polygon_area
from .model import IntelligentSlab


@dataclass(frozen=True, slots=True)
class SlabValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


class SlabValidator:
    def validate(self, slab: IntelligentSlab) -> SlabValidationResult:
        errors: list[str] = []
        gross = polygon_area(slab.boundary)
        if gross <= 0:
            errors.append("El contorno no tiene área")

        for opening in slab.openings:
            if polygon_area(opening.boundary) <= 0:
                errors.append(f"Hueco sin área: {opening.opening_id}")
            if not all(point_in_polygon(point, slab.boundary) for point in opening.boundary):
                errors.append(f"Hueco fuera del contorno: {opening.opening_id}")

        opening_area = sum(polygon_area(opening.boundary) for opening in slab.openings)
        if opening_area >= gross:
            errors.append("El área de huecos consume toda la losa")

        return SlabValidationResult(not errors, tuple(errors))
