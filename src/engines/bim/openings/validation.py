from __future__ import annotations

from dataclasses import dataclass

from .model import HostWallGeometry, Opening, OpeningState


@dataclass(frozen=True, slots=True)
class OpeningValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


class OpeningValidator:
    def validate(
        self,
        opening: Opening,
        wall: HostWallGeometry,
        *,
        clearance: float = 0.0,
    ) -> OpeningValidationResult:
        errors: list[str] = []

        if opening.host_wall_id != wall.wall_id:
            errors.append("El hueco no pertenece al muro indicado")

        if opening.placement.offset < clearance:
            errors.append("El hueco invade el borde inicial")

        if opening.placement.offset + opening.width > wall.length - clearance:
            errors.append("El hueco invade el borde final")

        if opening.placement.sill_height < 0:
            errors.append("La altura de antepecho no puede ser negativa")

        if opening.head_height > wall.height:
            errors.append("El hueco supera la altura del muro")

        valid = not errors
        opening.state = OpeningState.ACTIVE if valid else OpeningState.INVALID
        return OpeningValidationResult(valid, tuple(errors))
