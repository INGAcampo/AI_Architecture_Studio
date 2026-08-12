from __future__ import annotations

from .model import WallType


class WallTypeCatalog:
    def __init__(self) -> None:
        self._types: dict[str, WallType] = {}
        self.revision = 0

    def register(self, wall_type: WallType, *, replace: bool = False) -> None:
        if wall_type.type_id in self._types and not replace:
            raise KeyError(f"Tipo ya registrado: {wall_type.type_id}")
        self._types[wall_type.type_id] = wall_type
        self.revision += 1

    def get(self, type_id: str) -> WallType:
        try:
            return self._types[type_id]
        except KeyError as exc:
            raise KeyError(f"Tipo desconocido: {type_id}") from exc

    def remove(self, type_id: str) -> WallType:
        item = self.get(type_id)
        self._types.pop(type_id)
        self.revision += 1
        return item

    def duplicate(self, source_type_id: str, new_type_id: str, new_name: str) -> WallType:
        duplicate = self.get(source_type_id).duplicate(new_type_id, new_name)
        self.register(duplicate)
        return duplicate

    def all(self) -> tuple[WallType, ...]:
        return tuple(self._types[key] for key in sorted(self._types))
