from __future__ import annotations
import json
from pathlib import Path
from .entities import CadCircle, CadLine, CadPolyline
from .geometry import Point2D
from .scene import CadScene

class SceneSerializer:
    def save(self, scene: CadScene, path: Path) -> None:
        rows = []
        for entity in scene.all():
            base = {
                "id": entity.entity_id,
                "layer": entity.layer,
                "visible": entity.visible,
                "locked": entity.locked,
                "metadata": entity.metadata,
            }
            if isinstance(entity, CadLine):
                base.update({
                    "type": "line",
                    "start": [entity.start.x, entity.start.y],
                    "end": [entity.end.x, entity.end.y],
                })
            elif isinstance(entity, CadCircle):
                base.update({
                    "type": "circle",
                    "center": [entity.center.x, entity.center.y],
                    "radius": entity.radius,
                })
            elif isinstance(entity, CadPolyline):
                base.update({
                    "type": "polyline",
                    "points": [[p.x, p.y] for p in entity.points],
                    "closed": entity.closed,
                })
            rows.append(base)
        path.write_text(json.dumps({"entities": rows}, indent=2), encoding="utf-8")

    def load(self, path: Path) -> CadScene:
        data = json.loads(path.read_text(encoding="utf-8"))
        scene = CadScene()
        for row in data.get("entities", []):
            common = dict(
                entity_id=row["id"],
                layer=row.get("layer", "0"),
                visible=row.get("visible", True),
                locked=row.get("locked", False),
                metadata=row.get("metadata", {}),
            )
            if row["type"] == "line":
                entity = CadLine(
                    **common,
                    start=Point2D(*row["start"]),
                    end=Point2D(*row["end"]),
                )
            elif row["type"] == "circle":
                entity = CadCircle(
                    **common,
                    center=Point2D(*row["center"]),
                    radius=row["radius"],
                )
            else:
                entity = CadPolyline(
                    **common,
                    points=[Point2D(*p) for p in row["points"]],
                    closed=row.get("closed", False),
                )
            scene.add(entity)
        return scene
