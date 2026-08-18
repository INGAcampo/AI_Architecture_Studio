from __future__ import annotations
from dataclasses import dataclass, asdict, field
import hashlib, json
from pathlib import Path
from typing import Any

@dataclass
class ReportPackage:
    project_id: str
    metadata: dict[str, Any]
    documents: dict[str, dict[str, Any]] = field(default_factory=dict)
    schema: str = "aias.report_package.v1"

class ReportCore:
    """Evidence-bound deterministic documentation from canonical project artifacts."""
    def build(self, graph, standards, analysis_result, drawing_model, quantities) -> ReportPackage:
        if not graph.project_id or not graph.nodes: raise ValueError("report generation requires Project Graph")
        if analysis_result is None or drawing_model is None or quantities is None: raise ValueError("insufficient evidence for reports")
        metadata = {"project_id": graph.project_id, "project_name": graph.name, "jurisdiction": getattr(standards, "jurisdiction", None), "standards_pack": getattr(standards, "version", None), "revision": "V0"}
        nodes = graph.nodes
        areas = {n["name"]: n["properties"].get("area_m2") for n in nodes if n["type"] == "space" and n["properties"].get("area_m2") is not None}
        summary = {}
        for item in quantities.items: summary[item["material"]] = summary.get(item["material"], 0.0) + item["quantity"]
        docs = {
            "memoria_descriptiva": {"title": "Memoria descriptiva", "sections": {"project": metadata, "elements": len(nodes), "relationships": len(graph.relationships)}},
            "memoria_arquitectonica": {"title": "Memoria arquitectónica", "sections": {"spaces": areas, "levels": [n["name"] for n in nodes if n["type"] == "level"], "openings": [n["id"] for n in nodes if n["type"] in {"door", "window"}]}},
            "memoria_estructural": {"title": "Memoria estructural", "sections": {"status": analysis_result.status, "members": len(analysis_result.internal_forces), "code_checks": analysis_result.code_checks, "evidence_sha256": analysis_result.evidence_sha256}},
            "memoria_calculo_v0": {"title": "Memoria de cálculo V0", "sections": {"reactions": analysis_result.reactions, "displacements": analysis_result.displacements, "drifts": analysis_result.drifts, "internal_forces": analysis_result.internal_forces}},
            "especificaciones_tecnicas": {"title": "Especificaciones técnicas", "sections": {"materials": [n["properties"] for n in nodes if n["type"] == "material"], "source": "ProjectGraph/BIM"}},
            "resumen_materiales": {"title": "Resumen de materiales", "sections": summary},
            "resumen_boq": {"title": "Resumen de cantidades/BOQ", "sections": {"items": quantities.items, "evidence_sha256": _sha(quantities)}},
            "cuadro_de_areas": {"title": "Cuadro de áreas", "sections": areas},
            "reporte_normativo": {"title": "Reporte normativo", "sections": {"pack": getattr(standards, "version", None), "rules": list(getattr(standards, "rules", {}).keys()), "status": "TRACEABLE"}},
            "reporte_trazabilidad_evidencia": {"title": "Trazabilidad y evidencia", "sections": {"source_of_truth": ["ProjectGraph/BIM", "Standards", "Analysis", "Drawings", "Quantities"], "drawing_sheets": [s["number"] for s in drawing_model.sheets], "analysis_sha256": analysis_result.evidence_sha256, "quantity_sha256": _sha(quantities)}},
            "reporte_limitaciones": {"title": "Limitaciones", "sections": {"insufficient_evidence": [], "notes": ["V0 requiere revisión profesional y evidencia normativa completa antes de emitir planos ejecutivos."]}},
        }
        for doc in docs.values(): doc["evidence_sha256"] = _sha(doc["sections"])
        return ReportPackage(graph.project_id, metadata, docs)

    def export(self, package: ReportPackage, directory: str | Path) -> dict[str, str]:
        out = Path(directory); out.mkdir(parents=True, exist_ok=True); result = {}
        for name, doc in package.documents.items():
            payload = json.dumps({"metadata": package.metadata, "document": doc}, indent=2, sort_keys=True, ensure_ascii=False)
            (out / f"{name}.json").write_text(payload, encoding="utf-8")
            (out / f"{name}.md").write_text(f"# {doc['title']}\n\n```json\n{payload}\n```\n", encoding="utf-8")
            result[name] = _sha(payload)
        return result

def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(asdict(value) if hasattr(value, "__dataclass_fields__") else value, sort_keys=True, default=str).encode()).hexdigest()
