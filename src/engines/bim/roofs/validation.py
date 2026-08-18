from __future__ import annotations

from dataclasses import dataclass

from .geometry import point_in_polygon, polygon_area
from .model import IntelligentRoof


@dataclass(frozen=True, slots=True)
class RoofValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


class RoofValidator:
    def validate(self, roof: IntelligentRoof) -> RoofValidationResult:
        errors: list[str] = []
        gross = polygon_area(roof.boundary)
        if gross <= 0:
            errors.append("El contorno no tiene área")

        for opening in roof.openings:
            if polygon_area(opening.boundary) <= 0:
                errors.append(f"Hueco sin área: {opening.opening_id}")
            if not all(point_in_polygon(point, roof.boundary) for point in opening.boundary):
                errors.append(f"Hueco fuera del contorno: {opening.opening_id}")

        opening_area = sum(polygon_area(opening.boundary) for opening in roof.openings)
        if opening_area >= gross:
            errors.append("Los huecos consumen toda la cubierta")

        return RoofValidationResult(not errors, tuple(errors))
