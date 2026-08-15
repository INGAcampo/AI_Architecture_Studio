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
    annotations: list[dict[str, Any]] = field(default_factory=list)
    design_trace: dict[str, Any] = field(default_factory=dict)
    schema: str = "aias.drawing_model.v1"


class DrawingCore:
    """Deterministic BIM-derived drawing and sheet production foundation."""

    def build(
        self,
        graph: ProjectGraph,
        analysis_results: dict[str, Any] | None = None,
        reinforcement_model: Any | None = None,
    ) -> DrawingModel:
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
        if reinforcement_model is not None:
            self._bind_design(model, analysis_results, reinforcement_model)
        return model

    def _bind_design(
        self,
        model: DrawingModel,
        analysis_results: dict[str, Any],
        reinforcement_model: Any,
    ) -> None:
        reinforcement = (
            asdict(reinforcement_model)
            if hasattr(reinforcement_model, "__dataclass_fields__")
            else reinforcement_model
        )
        if not isinstance(reinforcement, dict):
            raise ValueError("INSUFFICIENT_EVIDENCE: reinforcement model required")
        required_hashes = {
            "analysis_evidence_sha256": reinforcement.get("analysis_evidence_sha256", ""),
            "standards_evidence_sha256": reinforcement.get("standards_evidence_sha256", ""),
            "design_evidence_sha256": reinforcement.get("design_evidence_sha256", ""),
        }
        if reinforcement.get("project_id") != model.project_id:
            raise ValueError("EVIDENCE_MISMATCH: drawing and design project ids differ")
        if analysis_results.get("status") != "PASS":
            raise ValueError("INSUFFICIENT_EVIDENCE: passing analysis required for design drawings")
        if any(len(value) != 64 for value in required_hashes.values()):
            raise ValueError("INSUFFICIENT_EVIDENCE: analysis, standards, and design SHA-256 required")
        if analysis_results.get("evidence_sha256") != required_hashes["analysis_evidence_sha256"]:
            raise ValueError("EVIDENCE_MISMATCH: analysis and design lineage differ")
        bar_sets = reinforcement.get("bar_sets") or []
        schedules = reinforcement.get("schedules") or []
        schedule_by_mark = {item.get("bar_mark"): item for item in schedules}
        if not bar_sets or len(schedule_by_mark) != len(bar_sets):
            raise ValueError("INSUFFICIENT_EVIDENCE: complete bar sets and schedules required")
        annotations = []
        for bar in sorted(bar_sets, key=lambda item: item.get("bar_mark", "")):
            mark = bar.get("bar_mark")
            schedule = schedule_by_mark.get(mark)
            if not mark or not schedule or schedule.get("bar_set_sha256") != bar.get("sha256"):
                raise ValueError("EVIDENCE_MISMATCH: bar set and schedule lineage differ")
            if any(bar.get(name) != value for name, value in required_hashes.items() if name != "design_evidence_sha256"):
                raise ValueError("EVIDENCE_MISMATCH: bar annotation lineage differs")
            sheet_number = "S-201" if bar.get("element_type") == "foundation" else "S-101"
            annotations.append({
                "id": f"annotation-{mark}",
                "kind": "reinforcement_annotation",
                "sheet_number": sheet_number,
                "bar_mark": mark,
                "element_id": bar.get("element_id"),
                "diameter_mm": bar.get("diameter_mm"),
                "quantity": bar.get("quantity"),
                "length_m": bar.get("length_m"),
                "spacing_mm": bar.get("spacing_mm"),
                "status": bar.get("status"),
                "bar_set_sha256": bar.get("sha256"),
                **required_hashes,
            })
        model.annotations = annotations
        model.design_trace = {
            **required_hashes,
            "bar_mark_count": len(annotations),
            "bar_marks_sha256": hashlib.sha256(
                json.dumps([item["bar_mark"] for item in annotations], separators=(",", ":")).encode()
            ).hexdigest(),
            "classification": "PRELIMINARY_NOT_FOR_CONSTRUCTION",
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
        }
        model.schema = "aias.drawing_model.v2"
        for sheet in model.sheets:
            sheet_annotations = [
                item["id"] for item in annotations if item["sheet_number"] == sheet["number"]
            ]
            sheet["annotation_ids"] = sheet_annotations
            sheet["metadata"]["design_trace"] = required_hashes
            sheet["metadata"]["classification"] = "PRELIMINARY_NOT_FOR_CONSTRUCTION"

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
        if model.design_trace:
            annotation_ids = {item.get("id") for item in model.annotations}
            linked_ids = {
                annotation_id
                for sheet in model.sheets
                for annotation_id in sheet.get("annotation_ids", [])
            }
            if not model.annotations: errors.append("design-bound drawing has no annotations")
            if annotation_ids != linked_ids: errors.append("drawing annotation-sheet linkage mismatch")
            if any(len(model.design_trace.get(name, "")) != 64 for name in (
                "analysis_evidence_sha256", "standards_evidence_sha256", "design_evidence_sha256"
            )): errors.append("drawing design lineage incomplete")
        return errors
