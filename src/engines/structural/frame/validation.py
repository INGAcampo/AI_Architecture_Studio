from __future__ import annotations

from dataclasses import dataclass

from .model import StructuralMember


@dataclass(frozen=True, slots=True)
class StructuralValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


class StructuralMemberValidator:
    def validate(self, member: StructuralMember) -> StructuralValidationResult:
        errors: list[str] = []
        if member.length <= 0:
            errors.append("Longitud inválida")
        if len(member.release_start) != 6 or len(member.release_end) != 6:
            errors.append("Las liberaciones deben contener seis grados de libertad")
        return StructuralValidationResult(not errors, tuple(errors))
