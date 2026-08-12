"""Deterministic repository audit for the AIAS professional desktop journeys."""
from __future__ import annotations

from pathlib import Path
from .models import Journey, JourneyRequirement


def _req(identifier: str, description: str, *paths: str) -> JourneyRequirement:
    return JourneyRequirement(identifier, description, tuple(paths))


JOURNEYS = (
    Journey("J01", "Create or resume a project", "A recoverable project is open with jurisdiction and units visible.", 3, (
        _req("project-lifecycle", "Create, open, save and recover projects.", "src/gui/project_management", "src/gui/main_window.py"),
        _req("project-navigation", "Navigate the project model.", "src/gui/project_browser", "src/gui/bim_workspace"),
        _req("workspace-persistence", "Restore the professional layout.", "src/gui/workspace/layout.py"),
    )),
    Journey("J02", "Model and inspect BIM", "A model element is created, selected and edited with undo.", 5, (
        _req("bim-tree", "Browse BIM entities and catalogs.", "src/gui/bim_workspace"),
        _req("properties", "Inspect and edit typed properties.", "src/gui/property_palette"),
        _req("undo", "Undo property mutations.", "src/gui/property_palette/history.py"),
        _req("commanding", "Invoke tools by command or ribbon.", "src/gui/command_line.py", "src/gui/ribbon.py"),
    )),
    Journey("J03", "Analyze, design and document a structure", "A normative calculation produces traceable drawings and a report.", 15, (
        _req("analysis", "Run structural analysis.", "src/structural_analysis", "src/engineering/structural"),
        _req("design", "Design structural members.", "src/structural_design", "src/design"),
        _req("drawing", "Generate engineering drawings.", "src/cad", "src/drawing"),
        _req("report", "Generate calculation evidence.", "src/calculation_reports", "src/reporting"),
    )),
    Journey("J04", "Coordinate disciplines", "Issues and model changes are reviewed with provenance.", 10, (
        _req("neutral-exchange", "Exchange neutral BIM/IFC data.", "src/aias_bim_ifc_sync", "src/ifc"),
        _req("coordination", "Coordinate issues and disciplines.", "src/coordination_dashboard", "src/collaboration"),
        _req("documents", "Maintain multiple document sessions.", "src/gui/workspace/manager.py"),
    )),
    Journey("J05", "Review and release evidence", "A reviewer can approve a versioned, reproducible deliverable.", 8, (
        _req("evidence", "Record verifiable evidence.", "src/aias_roadmap_audit", "src/evidence"),
        _req("governance", "Apply constitutional and SDD gates.", "src/aeps", "engineering/aeps"),
        _req("release", "Package a checksum-verifiable release.", "scripts", "src/release"),
    )),
    Journey("J06", "Learn in context", "The user reaches validated guidance without leaving the task context.", 2, (
        _req("knowledge", "Find governed project knowledge.", "src/aias_knowledge", "src/knowledge"),
        _req("university", "Open role-appropriate learning.", "src/aias_university", "engineering/aias/university"),
        _req("context-panel", "Show contextual knowledge in the workspace.", "src/gui/knowledge", "src/gui/ai_panel.py"),
    )),
)


def _exists(root: Path, candidate: str) -> bool:
    path = root / candidate
    return path.exists()


def evaluate_journey(root: Path, journey: Journey) -> dict:
    requirements = []
    for requirement in journey.requirements:
        found = tuple(path for path in requirement.evidence_any if _exists(root, path))
        requirements.append({
            "requirement_id": requirement.requirement_id,
            "description": requirement.description,
            "status": "EVIDENCED" if found else "MISSING",
            "evidence": list(found),
        })
    evidenced = sum(item["status"] == "EVIDENCED" for item in requirements)
    score = round(100 * evidenced / len(requirements))
    return {
        "journey_id": journey.journey_id,
        "name": journey.name,
        "outcome": journey.outcome,
        "target_minutes": journey.target_minutes,
        "evidence_score": score,
        "status": "EVIDENCED_NOT_USABILITY_VALIDATED" if score == 100 else "PARTIAL",
        "requirements": requirements,
    }


def audit_repository(root: Path) -> dict:
    results = [evaluate_journey(root, journey) for journey in JOURNEYS]
    return {
        "schema": "AIAS-UX-AUDIT-1.0",
        "method": "repository-evidence; no usability claim without observed sessions",
        "journeys": results,
        "aggregate_evidence_score": round(sum(item["evidence_score"] for item in results) / len(results)),
        "usability_validated": False,
        "next_gate": "rendered task-based usability sessions with representative users",
    }
