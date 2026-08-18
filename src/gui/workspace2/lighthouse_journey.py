"""Evidence-backed Workspace 2.0 journey for the Venezuelan lighthouse building."""
from __future__ import annotations

import hashlib
import html
import json
from dataclasses import dataclass
from pathlib import Path

from .commanding import ProfessionalStatus


@dataclass(frozen=True)
class JourneyStage:
    stage_id: str
    title: str
    status: str
    evidence: tuple[str, ...]
    summary: str


class LighthouseJourney:
    def __init__(self, dossier: Path):
        self.dossier = dossier.resolve()
        self._json = {}

    def _read(self, name: str) -> dict:
        path = self.dossier / name
        if not path.is_file():
            raise FileNotFoundError(f"missing_lighthouse_evidence:{name}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid_lighthouse_evidence:{name}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"invalid_lighthouse_evidence:{name}")
        self._json[name] = payload
        return payload

    def inspect(self) -> dict:
        brief = self._read("PROJECT_BRIEF.json")
        validation = self._read("VALIDATION.json")
        report = self._read("WHOLE_BUILDING_STRUCTURAL_REPORT.json")
        documentation = self._read("WHOLE_BUILDING_DOCUMENTATION_SUMMARY.json")
        thread = self._read("GOLDEN_THREAD.json")
        capabilities = self._read("JURISDICTION_CAPABILITY_MATRIX.json")
        required_files = {
            "model": "WHOLE_BUILDING_BIM_IFC_NEUTRAL.json",
            "plan": "whole_building_documents/STRUCTURAL_PLAN.svg",
            "elevation": "whole_building_documents/STRUCTURAL_ELEVATION.svg",
            "beams": "whole_building_documents/BEAM_SCHEDULE.csv",
            "columns": "whole_building_documents/COLUMN_SCHEDULE.csv",
            "foundations": "whole_building_documents/FOUNDATION_SCHEDULE.csv",
            "memory": "MEMORIA_DESCRIPTIVA.md",
        }
        missing = [relative for relative in required_files.values() if not (self.dossier / relative).is_file()]
        if missing:
            raise FileNotFoundError(f"missing_lighthouse_evidence:{','.join(missing)}")
        safe = (
            validation.get("safe_reference_status") is True
            and brief.get("normative_compliance_claimed") is False
            and brief.get("construction_approved") is False
            and report.get("construction_approved") is False
        )
        if not safe:
            raise ValueError("unsafe_lighthouse_claim_boundary")
        stages = (
            JourneyStage("context", "Project and jurisdiction", "COMPLETE", ("PROJECT_BRIEF.json", "JURISDICTION_CAPABILITY_MATRIX.json"), f'{brief["jurisdiction"]} · {brief["units"]} · {brief["legal_status"]}'),
            JourneyStage("model", "BIM / IFC neutral model", "COMPLETE_REFERENCE", (required_files["model"],), f'{report["model_summary"]["storeys"]} storeys · {report["model_summary"]["nodes"]} nodes · {report["model_summary"]["members"]} members'),
            JourneyStage("analysis", "Structural analysis", "COMPLETE_REFERENCE", ("WHOLE_BUILDING_STRUCTURAL_REPORT.json", "REFERENCE_LOAD_COMBINATIONS.json"), f'{report["analysis"]["member_demands"]} demands · {report["analysis"]["warnings"][0]}'),
            JourneyStage("design", "Member design and optimization", "COMPLETE_REFERENCE", ("WHOLE_BUILDING_STRUCTURAL_REPORT.json",), f'{report["design"]["members"]} members · max utilization {report["design"]["maximum_utilization"]:.2f}'),
            JourneyStage("documentation", "Drawings, schedules and quantities", "COMPLETE_REFERENCE", tuple(required_files[key] for key in ("plan", "elevation", "beams", "columns", "foundations", "memory")), f'{documentation["drawings"]} drawings · {documentation["schedules"]} schedules · {documentation["quantities"]["concrete_m3"]["total"]} m³ concrete'),
            JourneyStage("review", "Normative and professional release", "BLOCKED_EXTERNAL_AUTHORITY", ("GOLDEN_THREAD.json",), f'{len(capabilities["activation_dependencies"])} activation dependencies pending'),
        )
        evidence = sorted({item for stage in stages for item in stage.evidence})
        hashes = {relative: hashlib.sha256((self.dossier / relative).read_bytes()).hexdigest() for relative in evidence}
        status = ProfessionalStatus(
            jurisdiction=str(brief["jurisdiction_code"]), units=str(brief["units"]),
            normative_pack=str(brief["jurisdiction_profile_id"]), normative_status="NOT_ACQUIRED",
            review_status="REQUIRED", professional_reviewer=None,
        )
        return {
            "schema": "AIAS-LIGHTHOUSE-WORKSPACE-JOURNEY-1.0",
            "project_id": brief["project_id"], "title": brief["title"],
            "stages": [stage.__dict__ | {"evidence": list(stage.evidence)} for stage in stages],
            "professional_status": status.snapshot(), "safe_reference_status": safe,
            "golden_thread_complete": thread.get("complete") is True,
            "blocked_regulated_capabilities": capabilities["blocked_regulated_capabilities"],
            "activation_dependencies": capabilities["activation_dependencies"],
            "evidence_sha256": hashes,
        }

    def open_stage(self, stage_id: str, workspace) -> tuple:
        journey = self.inspect()
        stage = next((item for item in journey["stages"] if item["stage_id"] == stage_id), None)
        if stage is None:
            raise KeyError(f"unknown_lighthouse_stage:{stage_id}")
        documents = []
        for relative in stage["evidence"]:
            path = self.dossier / relative
            documents.append(workspace.open_document(str(path), metadata={"project_id": journey["project_id"], "stage_id": stage_id, "sha256": journey["evidence_sha256"][relative], "legal_status": "REFERENCE_ONLY"}))
        return tuple(documents)


def render_lighthouse_journey(data: dict) -> str:
    cards = "".join(f'<article class="{html.escape(stage["status"].lower())}"><small>{html.escape(stage["stage_id"].upper())}</small><h2>{html.escape(stage["title"])}</h2><b>{html.escape(stage["status"])}</b><p>{html.escape(stage["summary"])}</p><span>{len(stage["evidence"])} evidence files</span></article>' for stage in data["stages"])
    blocked = "".join(f"<li>{html.escape(item)}</li>" for item in data["blocked_regulated_capabilities"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AIAS · {html.escape(data["project_id"])}</title><style>:root{{--bg:#0B111A;--surface:#111B29;--raised:#172438;--border:#2B3C52;--text:#F5F7FA;--muted:#AFC0D4;--accent:#36A3FF;--ok:#3CCB7F;--warn:#FFB547}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 80% 0,#123b5e 0,transparent 32%),var(--bg);color:var(--text);font:14px Segoe UI,Arial,sans-serif}}header,main{{max-width:1320px;margin:auto}}header{{padding:34px 26px 22px;border-bottom:1px solid var(--border)}}small{{color:var(--accent);letter-spacing:1.4px}}h1{{font-size:30px;margin:8px 0}}header p,article p,article span{{color:var(--muted)}}main{{padding:24px 26px}}.status{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}}.status b{{background:var(--raised);border:1px solid var(--border);padding:8px 12px;border-radius:999px}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}article{{min-height:190px;background:linear-gradient(145deg,var(--raised),var(--surface));border:1px solid var(--border);border-radius:14px;padding:20px;box-shadow:0 12px 28px #0004}}article b{{color:var(--ok)}}article.blocked_external_authority b{{color:var(--warn)}}.warning{{margin-top:18px;padding:18px;border:1px solid #805d23;background:#ffb54712;border-radius:12px}}@media(max-width:850px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><header><small>AIAS // VENEZUELA STRUCTURAL LIGHTHOUSE</small><h1>{html.escape(data["title"])}</h1><p>Evidence-backed reference workflow. No normative compliance or construction approval is claimed.</p></header><main><div class="status"><b>VE</b><b>SI</b><b>REFERENCE ONLY</b><b>Golden thread: {str(data["golden_thread_complete"]).upper()}</b></div><section class="grid">{cards}</section><section class="warning"><h2>External authority gates remain visible</h2><ul>{blocked}</ul></section></main></body></html>'''
