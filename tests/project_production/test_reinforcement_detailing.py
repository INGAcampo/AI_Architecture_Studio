from aias_reinforcement_detailing import ReinforcementEngine
from aias_structural_professional import ProfessionalStructuralEngine
from aias_building_design_core import BuildingDesignCore

def result_with_structural_elements():
    g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot")); g.add_node("beam","B1"); g.add_node("column","C1"); e=ProfessionalStructuralEngine(); m=e.generate_3d_model(g); e.add_loads(m); e.apply_combinations(m); return e.analyze_and_design(m,{"pack":"VE"})

def test_bar_sets_schedule_and_traceability():
    r=result_with_structural_elements(); m=ReinforcementEngine().build(r,{"pack":"VE-PILOT-001.0"})
    assert m.bar_sets and m.schedules and ReinforcementEngine().total_steel_kg(m)>0
    assert all(len(b["sha256"])==64 for b in m.bar_sets)
    assert len(m.analysis_evidence_sha256)==64
    assert len(m.standards_evidence_sha256)==64
    assert len(m.design_evidence_sha256)==64
    assert all(row["bar_set_sha256"] in {bar["sha256"] for bar in m.bar_sets} for row in m.schedules)

def test_fails_closed_without_standards():
    try: ReinforcementEngine().build(result_with_structural_elements(),{})
    except ValueError as e: assert "INSUFFICIENT" in str(e)
    else: raise AssertionError("expected fail closed")

def test_fails_closed_without_passing_analysis():
    class FailedAnalysis:
        status="FAIL"
        evidence_sha256="0"*64
    try: ReinforcementEngine().build(FailedAnalysis(),{"pack":"VE-PILOT-001.0"})
    except ValueError as e: assert "INSUFFICIENT" in str(e)
    else: raise AssertionError("expected fail closed")
