from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any
from uuid import uuid4


ELEMENT_TYPES = {
    "site", "level", "grid", "space", "wall", "door", "window", "column",
    "beam", "slab", "stair", "roof", "foundation", "material"
}


@dataclass
class ProjectGraph:
    project_id: str
    name: str
    nodes: list[dict[str, Any]] = field(default_factory=list)
    relationships: list[dict[str, Any]] = field(default_factory=list)
    schema: str = "aias.project_graph.building.v1"

    def add_node(self, element_type: str, name: str, **properties: Any) -> str:
        if element_type not in ELEMENT_TYPES:
            raise ValueError(f"unsupported element type: {element_type}")
        node_id = properties.pop("id", f"{element_type}-{uuid4().hex[:12]}")
        node = {"id": node_id, "type": element_type, "name": name, "properties": properties}
        self.nodes.append(node)
        return node_id

    def relate(self, source: str, relation: str, target: str, **properties: Any) -> None:
        ids = {node["id"] for node in self.nodes}
        if source not in ids or target not in ids:
            raise KeyError("relationship endpoint is not in Project Graph")
        self.relationships.append({"source": source, "relation": relation, "target": target, "properties": properties})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "ProjectGraph":
        return cls(**json.loads(Path(path).read_text(encoding="utf-8")))


class BuildingDesignCore:
    """Canonical Project Graph → BIM foundation for PILOT-BUILDING-001."""

    def create_project(self, name: str, project_id: str = "PILOT-BUILDING-001") -> ProjectGraph:
        return ProjectGraph(project_id=project_id, name=name)

    def seed_pilot(self, graph: ProjectGraph) -> ProjectGraph:
        site = graph.add_node("site", "Pilot Site", jurisdiction="VE", units="SI", width_m=5.0, length_m=5.0)
        level = graph.add_node("level", "Level 1", elevation_m=0.0)
        grid = graph.add_node("grid", "Grid A", axis="A")
        material = graph.add_node("material", "Concrete C25", grade="C25/30")
        space = graph.add_node("space", "Main Space", area_m2=25.0)
        wall = graph.add_node("wall", "Wall W1", thickness_m=0.2, length_m=5.0, height_m=3.0)
        door = graph.add_node("door", "Door D1", width_m=0.9, height_m=2.1)
        window = graph.add_node("window", "Window WN1", width_m=1.2, height_m=1.2, sill_height_m=0.9)
        slab = graph.add_node("slab", "Slab S1", thickness_m=0.15)
        foundation = graph.add_node("foundation", "Foundation F1", system="isolated")
        for target in (level, grid, space): graph.relate(site, "contains", target)
        for target in (wall, slab, foundation): graph.relate(level, "hosts", target)
        graph.relate(space, "bounded_by", wall, opening_ids=[door, window])
        graph.relate(wall, "has_opening", door)
        graph.relate(wall, "has_opening", window)
        graph.relate(slab, "uses_material", material)
        graph.relate(foundation, "supports", slab)
        return graph

    def validate(self, graph: ProjectGraph) -> list[str]:
        errors: list[str] = []
        if not graph.project_id or not graph.name: errors.append("project identity is required")
        ids = [node["id"] for node in graph.nodes]
        if len(ids) != len(set(ids)): errors.append("duplicate node ids")
        if not any(node["type"] == "site" for node in graph.nodes): errors.append("site is required")
        for rel in graph.relationships:
            if rel["source"] not in ids or rel["target"] not in ids: errors.append("dangling relationship")
        return errors
