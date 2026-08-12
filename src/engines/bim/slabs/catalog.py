from __future__ import annotations

from .model import SlabType


class SlabTypeCatalog:
    def __init__(self) -> None:
        self._types: dict[str, SlabType] = {}
        self.revision = 0

    def register(self, slab_type: SlabType, *, replace: bool = False) -> None:
        if slab_type.type_id in self._types and not replace:
            raise KeyError(f"Tipo ya registrado: {slab_type.type_id}")
        self._types[slab_type.type_id] = slab_type
        self.revision += 1

    def get(self, type_id: str) -> SlabType:
        try:
            return self._types[type_id]
        except KeyError as exc:
            raise KeyError(f"Tipo desconocido: {type_id}") from exc

    def remove(self, type_id: str) -> SlabType:
        slab_type = self.get(type_id)
        self._types.pop(type_id)
        self.revision += 1
        return slab_type

    def all(self) -> tuple[SlabType, ...]:
        return tuple(self._types[key] for key in sorted(self._types))
