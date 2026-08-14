from aias_building_design_core import BuildingDesignCore
from aias_standards_core import StandardsPack
from aias_structural_core import StructuralAnalysisCore
from aias_drawing_core import DrawingCore
from aias_quantities_core import QuantityTakeoffEngine
from aias_reports_core import ReportCore
from aias_qa_core import QACore

def artifacts():
    g = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot")); s = StructuralAnalysisCore(); m = s.generate_model(g); s.add_load_case(m,"dead",100); s.apply_ve_combinations(m); r = s.solve_linear(m,{"source":"VE"}); d = DrawingCore().build(g,{"status":r.status}); q = QuantityTakeoffEngine().build(g); p = ReportCore().build(g,StandardsPack(),r,d,q); return g, StandardsPack(), m, r, d, q, p

def test_end_to_end_gate_and_finding():
    g, st, m, r, d, q, p = artifacts(); qa = QACore().validate(g,st,m,r,d,q,p); assert qa.gate == "READY_FOR_PILOT_ISSUANCE"; assert qa.score["critical_blockers"] == 0
    g.relationships.append({"source":"bad","relation":"hosts","target":"bad"}); qa = QACore().validate(g,st,m,r,d,q,p); assert any(f.severity == "CRITICAL" for f in qa.findings)

def test_bounded_design_loop():
    g, st, m, r, d, q, p = artifacts(); calls = []
    def validate(_): calls.append(1); return QAPackage("PILOT-BUILDING-001", gate="NOT_READY")
    from aias_qa_core.qa import QAPackage
    out = QACore().design_loop(g, lambda x: None, validate, 2); assert len(calls) == 1 and len(out.audit_trail) >= 1
