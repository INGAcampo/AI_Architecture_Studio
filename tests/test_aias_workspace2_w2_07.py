from pathlib import Path
from gui.workspace2.experience_validation import UsabilitySessionEvidence,audit_design_contrast,audit_html,audit_qss_performance,build_automated_report
ROOT=Path(__file__).resolve().parents[1]
def test_semantic_color_pairs_meet_governed_contrast():
 result=audit_design_contrast();assert result["passed"],result["results"]
def test_generated_workspace_pages_meet_semantic_and_size_budgets():
 for name in ("workspace2_w2_05_outputs/LIGHTHOUSE_JOURNEY.html","workspace2_w2_06_outputs/COORDINATION_LEARNING.html"):assert audit_html(ROOT/name)["passed"],audit_html(ROOT/name)["issues"]
def test_qss_generation_meets_interaction_budget():assert audit_qss_performance()["passed"]
def test_human_session_evidence_fails_closed():
 required=("T01","T02");bad=UsabilitySessionEvidence("S1","Engineer","","2026-08-04",({"task_id":"T01","outcome":"PASS","elapsed_seconds":10},),"");assert "incomplete_session_identity" in bad.validate(required);assert "incomplete_or_duplicate_tasks" in bad.validate(required)
def test_automated_report_does_not_claim_representative_validation():
 report=build_automated_report(ROOT);assert report["automated_gates_passed"];assert report["representative_sessions_completed"]==0;assert not report["representative_usability_validated"]
