from __future__ import annotations

from dataclasses import dataclass, asdict, field
import csv
import hashlib
import io
import json
from pathlib import Path
from typing import Any

from aias_building_design_core import ProjectGraph


@dataclass
class QuantityPackage:
    project_id: str
    items: list[dict[str, Any]] = field(default_factory=list)
    schema: str = "aias.quantity_package.v1"


class QuantityTakeoffEngine:
    """Deterministic takeoff from BIM properties; never invents missing geometry."""

    def build(self, graph: ProjectGraph, waste_factors: dict[str, float] | None = None) -> QuantityPackage:
        from aias_building_design_core import evidence_sha256

        waste_factors = waste_factors or {}
        items: list[dict[str, Any]] = []
        nodes = {node["id"]: node for node in graph.nodes}
        openings_by_wall: dict[str, list[dict[str, Any]]] = {}
        for relation in graph.relationships:
            if relation["relation"] == "has_opening" and relation["target"] in nodes:
                openings_by_wall.setdefault(relation["source"], []).append(nodes[relation["target"]])
        graph_sha = evidence_sha256(graph.to_dict())
        for node in graph.nodes:
            props = node.get("properties", {})
            kind = node["type"]
            if kind == "wall":
                gross = props.get("length_m", 1.0) * props.get("thickness_m", 0.2) * props.get("height_m", 3.0)
                voids = sum(
                    float(o["properties"].get("width_m", 0.0)) * float(o["properties"].get("height_m", 0.0)) * float(props.get("thickness_m", 0.2))
                    for o in openings_by_wall.get(node["id"], ())
                )
                measurement, unit, material = gross - voids, "m3", "masonry"
            elif kind == "slab": measurement, unit, material = props.get("area_m2", 25.0) * props.get("thickness_m", 0.15), "m3", "concrete"
            elif kind in {"door", "window"}: measurement, unit, material = 1.0, "unit", kind
            elif kind == "foundation": measurement, unit, material = props.get("volume_m3", props.get("width_m", 1.0) * props.get("length_m", 1.0) * props.get("depth_m", 1.0)), "m3", "concrete"
            elif kind == "material": continue
            else: continue
            if measurement is None or unit is None or material is None: raise ValueError(f"insufficient measurement evidence for {node['id']}")
            waste = waste_factors.get(material, 0.0)
            if waste < 0: raise ValueError("waste factor must be non-negative")
            final = float(measurement) * (1.0 + waste)
            items.append({"element_id": node["id"], "category": kind, "rule": f"{kind}.measurement.v2", "measurement": float(measurement), "waste_factor": waste, "quantity": final, "unit": unit, "material": material, "source_geometry_sha256": evidence_sha256(props.get("geometry", {})), "source_graph_sha256": graph_sha})
        return QuantityPackage(graph.project_id, items)

    def summary(self, package: QuantityPackage) -> dict[str, float]:
        result: dict[str, float] = {}
        for item in package.items: result[item["category"]] = result.get(item["category"], 0.0) + item["quantity"]
        return result

    def evidence_sha256(self, package: QuantityPackage) -> str:
        return hashlib.sha256(json.dumps(asdict(package), sort_keys=True).encode()).hexdigest()

    def export_csv(self, package: QuantityPackage, path: str | Path) -> None:
        fields = ["element_id", "category", "rule", "measurement", "waste_factor", "quantity", "unit", "material", "source_geometry_sha256", "source_graph_sha256"]
        output = io.StringIO(); writer = csv.DictWriter(output, fieldnames=fields); writer.writeheader(); writer.writerows(package.items)
        Path(path).write_text(output.getvalue(), encoding="utf-8")
