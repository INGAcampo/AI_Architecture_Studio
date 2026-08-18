from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BridgeEntityRef:
    source: str
    entity_id: str
    entity_type: str
    global_id: str | None = None


@dataclass(frozen=True)
class BridgeTopologySummary:
    solids: int = 0
    shells: int = 0
    faces: int = 0
    wires: int = 0
    edges: int = 0
    vertices: int = 0


@dataclass(frozen=True)
class BridgeMesh:
    vertices: tuple[tuple[float, float, float], ...]
    triangles: tuple[tuple[int, int, int], ...]

    def validate(self) -> None:
        if not self.vertices:
            raise ValueError("mesh must contain vertices")
        for tri in self.triangles:
            if len(tri) != 3:
                raise ValueError("triangles must contain exactly three indices")
            for index in tri:
                if index < 0 or index >= len(self.vertices):
                    raise ValueError("triangle index is outside the vertex array")


@dataclass(frozen=True)
class BridgeGeometryPayload:
    entity: BridgeEntityRef
    geometry_kind: str
    topology: BridgeTopologySummary
    mesh: BridgeMesh | None
    native_shape: Any | None
    metadata: dict[str, Any]
