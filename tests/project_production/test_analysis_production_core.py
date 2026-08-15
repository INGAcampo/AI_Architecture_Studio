import copy

from aias_project_intake.builders import ParametricProjectGraphBuilder
from aias_project_production.certification import certify_analysis_production_core
from aias_structural_professional import ProfessionalStructuralEngine


def _manifest(project_id: str, width_m: float = 8.0) -> dict:
    return {
        "project_id": project_id,
        "project_name": project_id,
        "mode": "PILOT_SYNTHETIC",
        "scenario_id": "NOMINAL_CASE_001",
        "SYNTHETIC_TEST_DATA": True,
        "NOT_FOR_CONSTRUCTION": True,
        "building_program": {
            "levels": 2,
            "width_m": width_m,
            "length_m": 9.0,
            "storey_height_m": 3.0,
        },
    }


def _analyze(project_id: str = "ANALYSIS-TRACE", width_m: float = 8.0):
    graph = ParametricProjectGraphBuilder().build(_manifest(project_id, width_m))
    engine = ProfessionalStructuralEngine()
    model = engine.generate_3d_model(graph)
    engine.add_loads(model)
    engine.apply_combinations(model)
    standards = {
        "pack": "AIAS-SYNTHETIC-ANALYSIS-001",
        "SYNTHETIC_TEST_DATA": True,
        "NOT_FOR_CONSTRUCTION": True,
    }
    return engine, model, standards, engine.analyze_and_design(model, standards)


def test_analysis_materializes_combinations_equilibrium_and_lineage():
    _, model, _, result = _analyze()

    assert result.status == "PASS"
    assert set(result.combination_results) == {"VE-ULS-1", "VE-SLS-1"}
    assert all(
        item["equilibrium_status"] == "PASS"
        for item in result.combination_results.values()
    )
    assert result.analysis_trace["source_graph_sha256"] == model.metadata["source_graph_sha256"]
    assert result.analysis_trace["governing_combination"] == "VE-ULS-1"
    assert all(
        envelope["governing_combination"] == "VE-ULS-1"
        for envelope in result.load_envelopes.values()
    )


def test_analysis_is_deterministic_and_geometry_sensitive():
    engine, model, standards, first = _analyze("ANALYSIS-A", 8.0)
    repeated = engine.analyze_and_design(copy.deepcopy(model), copy.deepcopy(standards))
    _, _, _, wider = _analyze("ANALYSIS-B", 11.0)

    assert first.evidence_sha256 == repeated.evidence_sha256
    assert first.evidence_sha256 != wider.evidence_sha256
    assert (
        first.combination_results["VE-ULS-1"]["factored_total_kN"]
        != wider.combination_results["VE-ULS-1"]["factored_total_kN"]
    )


def test_analysis_fails_closed_for_missing_supports_or_standards():
    engine, model, standards, _ = _analyze("ANALYSIS-FAIL-CLOSED")
    assert engine.analyze_and_design(model, {}).status == "INSUFFICIENT_EVIDENCE"
    for node in model.nodes:
        node["support"] = False
    result = engine.analyze_and_design(model, standards)
    assert result.status == "INSUFFICIENT_EVIDENCE"
    assert result.limitations == ["analysis model has no supports"]


def test_analysis_certification_uses_two_isolated_synthetic_projects(tmp_path):
    certification = certify_analysis_production_core(tmp_path)

    assert certification["verdict"] == "ANALYSIS_PRODUCTION_CORE_READY"
    assert all(certification["checks"].values())
    assert certification["estimated_time_reduction_percent"] >= 45
    assert {item["project_id"] for item in certification["projects"]} == {
        "ANALYSIS-CORE-CERT-A",
        "ANALYSIS-CORE-CERT-B",
    }
