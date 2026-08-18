from aias_building_design_core import BuildingDesignCore
from aias_structural_core import StructuralAnalysisCore


def test_analysis_model_and_linear_result_are_traceable():
    graph = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot Building"))
    core = StructuralAnalysisCore()
    model = core.generate_model(graph)
    core.add_load_case(model, "dead", 100.0)
    core.add_load_case(model, "live", 50.0)
    core.apply_ve_combinations(model)
    result = core.solve_linear(model, {"pack": "VE-PILOT-001.0"})
    assert result.status == "PASS"
    assert result.reactions and result.internal_forces and len(result.evidence_sha256) == 64


def test_solver_fails_closed_without_inputs():
    assert StructuralAnalysisCore().solve_linear(StructuralAnalysisCore().generate_model(BuildingDesignCore().create_project("x"))).status == "INSUFFICIENT_EVIDENCE"
