from pathlib import Path
from aias_roadmap_audit import IntegralRoadmapAuditor
ROOT=Path(__file__).resolve().parents[1]
def test_integral_audit_proves_current_technical_macrodeliveries():
 r=IntegralRoadmapAuditor().audit(ROOT);assert r["technical_macrodeliveries_complete"] is True;assert r["materialization"]["pending"]==[];assert r["structural"]["implemented"]==20;assert len(r["giant_steps"])==9;assert r["installers"]["all_valid"]
def test_integral_audit_keeps_external_gates_explicit():
 r=IntegralRoadmapAuditor().audit(ROOT);assert {x["macrodelivery"] for x in r["external_gates"]}=={"G2","G3","G4","G9"};assert any(x["id"]=="FUTURE-000002" for x in r["materialization"]["specified"])
