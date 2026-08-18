from pathlib import Path
from gui.workspace2 import CoordinationLearningHub,render_coordination_learning
ROOT=Path(__file__).resolve().parents[1]
def test_lighthouse_coordination_is_blocked_with_real_evidence():
 data=CoordinationLearningHub(ROOT).build_lighthouse();coord=data["coordination"];assert coord["release_readiness"]=="BLOCKED";assert "VE-NORMATIVE-001:critical_open" in coord["blocking_reasons"];assert "INT-GEO-STR:unresolved_interface" in coord["blocking_reasons"];assert not data["release_authorized"]
def test_every_blocker_has_contextual_versioned_learning():
 data=CoordinationLearningHub(ROOT).build_lighthouse();assert len(data["contextual_learning"])==len(data["coordination"]["blocking_reasons"]);assert data["course_version"]=="1.0.0";assert all(item["not_a_professional_license"] and len(item["resource_sha256"])==64 for item in data["contextual_learning"])
def test_combined_panel_preserves_professional_boundary():
 page=render_coordination_learning(CoordinationLearningHub(ROOT).build_lighthouse());assert "<!doctype html>" in page;assert "Incidencias y evidencia" in page;assert "Aprendizaje recomendado" in page;assert "no sustituye normas oficiales ni licencia profesional" in page
