from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from .entities import CadEntity

@dataclass(slots=True)
class BlockDefinition:
    name: str
    entities: list[CadEntity] = field(default_factory=list)

class BlockLibrary:
    def __init__(self) -> None:
        self._blocks: dict[str, BlockDefinition] = {}

    def add(self, block: BlockDefinition) -> None:
        if block.name in self._blocks:
            raise ValueError(f"Block exists: {block.name}")
        self._blocks[block.name] = block

    def instantiate(self, name: str) -> list[CadEntity]:
        return deepcopy(self._blocks[name].entities)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._blocks))
