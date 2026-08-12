"""Coordination evidence joined to contextual AIAS University learning."""
from __future__ import annotations

import hashlib
import html
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from aias_structural_codes_program import CoordinationDashboardEngine, CoordinationInterface, CoordinationIssue, DisciplineStatus
from aias_university.catalog import UniversityCatalog


@dataclass(frozen=True)
class LearningRecommendation:
    blocker: str
    course_id: str
    lesson_id: str
    title: str
    resource: str
    resource_sha256: str
    not_a_professional_license: bool = True


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CoordinationLearningHub:
    def __init__(self, root: Path):
        self.root = root.resolve()
        inventory = json.loads((self.root / "engineering/aias/master/inventory/AIAS_MASTER_CONCEPT_INVENTORY.json").read_text(encoding="utf-8"))
        assets = {item["id"] for item in inventory["concepts"]}
        self.catalog = UniversityCatalog(self.root / "engineering/aias/university/AIAS_UNIVERSITY_CATALOG.json", assets)

    def _evidence(self, relative: str) -> tuple[str, str]:
        candidate = (self.root / relative).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("evidence_outside_repository") from exc
        if not candidate.is_file():
            raise FileNotFoundError(f"missing_contextual_evidence:{relative}")
        return relative, _digest(candidate)

    def build_lighthouse(self) -> dict:
        dossier = "lighthouse000001_venezuela_outputs/technical_dossier"
        sources = {
            "STRUCTURAL": f"{dossier}/WHOLE_BUILDING_STRUCTURAL_REPORT.json",
            "BIM": f"{dossier}/WHOLE_BUILDING_BIM_IFC_NEUTRAL.json",
            "GEOTECHNICAL": f"{dossier}/PROJECT_BRIEF.json",
            "HYDRAULIC": f"{dossier}/JURISDICTION_CAPABILITY_MATRIX.json",
            "CIVIL": f"{dossier}/JURISDICTION_CAPABILITY_MATRIX.json",
        }
        evidence = {discipline: self._evidence(path) for discipline, path in sources.items()}
        disciplines = tuple(DisciplineStatus(name, f"LIGHTHOUSE-{name}", "R01", evidence[name][1], "VALIDATED" if name in {"STRUCTURAL", "BIM"} else "WARNING", 0 if name in {"STRUCTURAL", "BIM"} else 1) for name in sorted(sources))
        interfaces = (
            CoordinationInterface("INT-STR-BIM", "STRUCTURAL", "BIM", "RESOLVED", sources["BIM"]),
            CoordinationInterface("INT-GEO-STR", "GEOTECHNICAL", "STRUCTURAL", "OPEN", sources["GEOTECHNICAL"]),
        )
        issues = (
            CoordinationIssue("VE-NORMATIVE-001", "STRUCTURAL", "CRITICAL", "OPEN", "Licensed Venezuelan normative pack and professional approval are pending.", f"{dossier}/JURISDICTION_CAPABILITY_MATRIX.json"),
            CoordinationIssue("SITE-GEO-001", "GEOTECHNICAL", "HIGH", "OPEN", "Site-specific geotechnical investigation is absent.", f"{dossier}/PROJECT_BRIEF.json"),
        )
        snapshot = CoordinationDashboardEngine().build("LIGHTHOUSE-000001", "R01", disciplines, interfaces, issues)
        course = self.catalog.get("COURSE-AIAS-LIGHTHOUSE-COORD-001")
        lesson_by_blocker = {
            "unresolved_interface": "LESSON-LH-002",
            "critical_open": "LESSON-LH-003",
        }
        lessons = {lesson["lesson_id"]: lesson for module in course["modules"] for lesson in module["lessons"]}
        recommendations = []
        for blocker in snapshot.blocking_reasons:
            lesson_id = next((lesson for marker, lesson in lesson_by_blocker.items() if marker in blocker), "LESSON-LH-001")
            lesson = lessons[lesson_id]; resource, digest = self._evidence(lesson["resource"])
            recommendations.append(LearningRecommendation(blocker, course["course_id"], lesson_id, lesson["title"], resource, digest))
        return {
            "schema": "AIAS-WORKSPACE2-COORDINATION-LEARNING-1.0",
            "coordination": asdict(snapshot),
            "contextual_learning": [asdict(item) for item in recommendations],
            "course_version": course["version"],
            "release_authorized": False,
            "professional_release_required": True,
        }


def render_coordination_learning(data: dict) -> str:
    coordination = data["coordination"]
    issues = "".join(f'<article><b>{html.escape(item["issue_id"])}</b><span>{html.escape(item["severity"])} · {html.escape(item["status"])}</span><p>{html.escape(item["description"])}</p><small>{html.escape(item["evidence_locator"])}</small></article>' for item in coordination["issues"])
    lessons = "".join(f'<article><b>{html.escape(item["lesson_id"])}</b><span>AIAS University · internal competency</span><p>{html.escape(item["title"])}</p><small>{html.escape(item["resource"])}</small></article>' for item in data["contextual_learning"])
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AIAS Coordination + Learning</title><style>:root{{--bg:#0B111A;--surface:#111B29;--raised:#172438;--border:#2B3C52;--text:#F5F7FA;--muted:#AFC0D4;--accent:#36A3FF;--warn:#FFB547}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px Segoe UI,Arial,sans-serif}}header,main{{max-width:1280px;margin:auto}}header{{padding:32px 24px;border-bottom:1px solid var(--border)}}h1{{margin:8px 0}}header small{{color:var(--accent)}}main{{padding:24px}}.gate{{padding:14px;border:1px solid #805d23;background:#ffb54712;color:var(--warn);border-radius:10px}}.columns{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}}section{{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px}}article{{background:var(--raised);border:1px solid var(--border);padding:14px;border-radius:10px;margin-top:10px}}article span,article small{{display:block;color:var(--muted);margin-top:5px}}@media(max-width:800px){{.columns{{grid-template-columns:1fr}}}}</style></head><body><header><small>AIAS // COORDINATION + CONTEXTUAL LEARNING</small><h1>{html.escape(coordination["project_id"])} · {html.escape(coordination["revision"])}</h1><p>{html.escape(coordination["release_readiness"])}</p></header><main><div class="gate">La formación contextual ayuda a resolver el trabajo; no sustituye normas oficiales ni licencia profesional.</div><div class="columns"><section><h2>Incidencias y evidencia</h2>{issues}</section><section><h2>Aprendizaje recomendado</h2>{lessons}</section></div></main></body></html>'''
