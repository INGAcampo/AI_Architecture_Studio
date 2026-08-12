from __future__ import annotations
from .entities import CadEntity
from .layers import LayerManager

class CadScene:
    def __init__(self) -> None:
        self.layers = LayerManager()
        self._entities: dict[str, CadEntity] = {}

    def add(self, entity: CadEntity) -> str:
        if entity.entity_id in self._entities:
            raise ValueError("Duplicate entity id.")
        if entity.layer not in self.layers.names():
            raise ValueError(f"Unknown layer: {entity.layer}")
        self._entities[entity.entity_id] = entity
        return entity.entity_id

    def remove(self, entity_id: str) -> CadEntity:
        return self._entities.pop(entity_id)

    def get(self, entity_id: str) -> CadEntity:
        return self._entities[entity_id]

    def all(self) -> tuple[CadEntity, ...]:
        return tuple(self._entities.values())

    def by_layer(self, name: str) -> tuple[CadEntity, ...]:
        return tuple(e for e in self._entities.values() if e.layer == name)
