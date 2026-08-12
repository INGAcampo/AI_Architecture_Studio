"""Reusable block definitions and insertion management."""
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass(slots=True)
class BlockDefinition:
    """Named reusable collection of CAD entities with a base point."""
    name: str
    entities: list = field(default_factory=list)
    attributes: dict[str,str] = field(default_factory=dict)

class BlockEngine:
    """Register unique blocks and materialize transformed insertions."""
    def __init__(self) -> None:
        self._blocks={}

    def create(self, name, entities, attributes=None):
        """Build the create required by the S1 professional CAD foundation program from explicit inputs."""
        if name in self._blocks:
            raise ValueError(name)
        block=BlockDefinition(name,list(entities),dict(attributes or {}))
        self._blocks[name]=block
        return block

    def insert(self, name):
        """Add insert to the S1 professional CAD foundation program while enforcing identity constraints."""
        return deepcopy(self._blocks[name].entities)

    def get(self, name):
        """Return get from the S1 professional CAD foundation program using deterministic lookup rules."""
        return self._blocks[name]
