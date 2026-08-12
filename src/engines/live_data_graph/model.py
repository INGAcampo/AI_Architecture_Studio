"""Modelos tipados del AIAS Live Data Graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


class NodeState(str, Enum):
    """Estado operativo de un nodo dentro del grafo."""

    CLEAN = "clean"
    DIRTY = "dirty"
    PROCESSING = "processing"
    ERROR = "error"


@dataclass(slots=True)
class DataNode:
    """Unidad direccionable del grafo de datos de AIAS."""

    node_id: str
    kind: str
    payload: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    state: NodeState = NodeState.CLEAN
    revision: int = 0

    def __post_init__(self) -> None:
        self.node_id = str(self.node_id).strip()
        self.kind = str(self.kind).strip()
        if not self.node_id:
            raise ValueError("node_id no puede estar vacío.")
        if not self.kind:
            raise ValueError("kind no puede estar vacío.")


@dataclass(frozen=True, slots=True)
class GraphChange:
    """Descripción inmutable de una propagación realizada por el grafo."""

    source_id: str
    affected_ids: tuple[str, ...]
    revision: int
    reason: str = "update"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )
