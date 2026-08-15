from __future__ import annotations

from dataclasses import dataclass, asdict, field
import hashlib
import json
from pathlib import Path
from typing import Any

from aias_building_design_core import ProjectGraph


@dataclass
class DrawingModel:
    project_id: str
    views: list[dict[str, Any]] = field(default_factory=list)
    sheets: list[dict[str, Any]] = field(default_factory=list)
    schema: str = "aias.drawing_model.v1"


class DrawingCore:
    """Deterministic BIM-derived drawing and sheet production foundation."""

    def build(self, graph: ProjectGraph, analysis_results: dict[str, Any] | None = None) -> DrawingModel:
        from aias_building_design_core import evidence_sha256

        if not graph.nodes or not any(node["type"] == "level" for node in graph.nodes):
            raise ValueError("drawing generation requires Project Graph levels")
        if analysis_results is None:
            raise ValueError("drawing generation requires analysis results")
        model = DrawingModel(graph.project_id)
        views = [("A-101", "Architectural Plan", "plan", "1:100"), ("S-101", "Structural Plan", "plan", "1:100"), ("S-201", "Foundation Plan", "foundation", "1:100"), ("A-301", "Building Section", "section", "1:100"), ("A-401", "Building Elevation", "elevation", "1:100")]
        node_ids = [node["id"] for node in graph.nodes]
        graph_sha = evidence_sha256(graph.to_dict())
        geometry_trace = {
            node["id"]: evidence_sha256(node.get("properties", {}).get("geometry", {}))
            for node in graph.nodes
        }
        for number, title, kind, scale in views:
            view = {"id": f"view-{number}", "number": number, "title": title, "kind": kind, "scale": scale, "source_node_ids": node_ids, "source_graph_sha256": graph_sha, "source_geometry_sha256": geometry_trace}
            model.views.append(view)
            model.sheets.append({"id": f"sheet-{number}", "number": number, "title": title, "view_ids": [view["id"]], "metadata": {"project_id": graph.project_id, "source": "ProjectGraph/BIM"}})
        return model

    def export_pdf(self, model: DrawingModel, path: str | Path) -> str:
        payload = json.dumps(asdict(model), sort_keys=True, indent=2).encode()
        digest = hashlib.sha256(payload).hexdigest()
        pdf = b"%PDF-1.4\n% AIAS DRAWING INDEX\n" + payload + b"\n%%EOF\n"
        Path(path).write_bytes(pdf)
        return digest

    def validate(self, model: DrawingModel) -> list[str]:
        errors = []
        if not model.views or not model.sheets: errors.append("drawing model has no views or sheets")
        if len(model.views) != len(model.sheets): errors.append("view-sheet cardinality mismatch")
        for sheet in model.sheets:
            if not sheet.get("view_ids") or not sheet.get("metadata", {}).get("project_id"): errors.append("sheet metadata incomplete")
        return errors
