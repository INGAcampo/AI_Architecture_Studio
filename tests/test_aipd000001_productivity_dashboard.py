import json
from pathlib import Path
from aias_productivity_dashboard.collector import collect
from aias_productivity_dashboard.model import acceleration_status,maturity_status
from aias_productivity_dashboard.orchestrator import ProductivityDashboardOrchestrator
from aias_productivity_dashboard.renderer import render
ROOT=Path(__file__).resolve().parents[1]
def test_acceleration_target():assert acceleration_status(.55,"REFERENCE_ENGINEERING_ESTIMATE")["meets_target"]
def test_level_five_reference_is_not_audit():assert maturity_status(5,None)["level_5_reference"] and not maturity_status(5,None)["level_5_organizationally_audited"]
def test_collector_uses_repository_evidence():
 d=collect(ROOT);assert d["capital"]["components"]>100 and d["governance"]["components"]>=6 and d["maturity"]["campaign_status"]=="ACTIVE_EVIDENCE_COLLECTION" and not d["certification"]["externally_certified"]
def test_company_map_contains_declared_systems():
 names={x["name"] for x in collect(ROOT)["company_systems"]};assert {"Constitución","PMO","Sistema nervioso","Academia","Observatorio tecnológico"}<=names
def test_experience_panel_is_evidence_bounded():
 d=collect(ROOT);assert d["experience"]["workspace_current"]=="AIAS-WORKSPACE-2.0-W2-07";assert d["experience"]["ux_evidence_percent"]==65;assert d["experience"]["representative_sessions"]==0;assert not d["experience"]["rendered_usability_validated"];assert d["experience"]["offline_media_verified"] and d["experience"]["offline_installers"]==7;assert not d["experience"]["publisher_signed"] and not d["experience"]["iso_image_created"]
def test_external_gate_panel_uses_ledger_and_authority_evidence():
 d=collect(ROOT);assert d["external_gates"]["total"]==4;assert d["external_gates"]["satisfied"]==0;assert d["external_gates"]["evidence_records"]==0;assert d["external_gates"]["registered_authorities"]==0
def test_renderer_is_self_contained():
 h=render(collect(ROOT));assert "<!doctype html>" in h and "AIAS Productivity Dashboard" in h and "aias-evidence" in h and "Compuertas externas verificables" in h
def test_orchestrator_writes_snapshot_panel_and_release(tmp_path):
 r=ProductivityDashboardOrchestrator().execute(ROOT,tmp_path);assert r["validated"] and Path(r["panel"]).is_file() and Path(r["archive"]).is_file() and len(r["sha256"])==64 and json.loads(Path(r["snapshot"]).read_text())["identity"]["name"]=="AIAS Productivity Dashboard"
