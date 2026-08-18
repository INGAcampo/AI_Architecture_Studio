from __future__ import annotations

from .model import RoofType


class RoofTypeCatalog:
    def __init__(self) -> None:
        self._types: dict[str, RoofType] = {}
        self.revision = 0

    def register(self, roof_type: RoofType, *, replace: bool = False) -> None:
        if roof_type.type_id in self._types and not replace:
            raise KeyError(f"Tipo ya registrado: {roof_type.type_id}")
        self._types[roof_type.type_id] = roof_type
        self.revision += 1

    def get(self, type_id: str) -> RoofType:
        try:
            return self._types[type_id]
        except KeyError as exc:
            raise KeyError(f"Tipo desconocido: {type_id}") from exc

    def remove(self, type_id: str) -> RoofType:
        roof_type = self.get(type_id)
        self._types.pop(type_id)
        self.revision += 1
        return roof_type

    def all(self) -> tuple[RoofType, ...]:
        return tuple(self._types[key] for key in sorted(self._types))
