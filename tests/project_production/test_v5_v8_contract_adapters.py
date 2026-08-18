from aias_building_design_core import BuildingDesignCore
from aias_structural_professional import ProfessionalStructuralEngine
from aias_project_production.adapters import DrawingProductionAdapter, QuantityWorkbookAdapter, ReportProductionAdapter, ProfessionalQAAdapter, ExecutiveIssuanceAdapter


def test_contract_adapters_preserve_canonical_ids_and_fail_closed(tmp_path):
    core = BuildingDesignCore(); graph = core.seed_pilot(core.create_project("Synthetic"))
    engine = ProfessionalStructuralEngine(); model = engine.generate_3d_model(graph); engine.add_loads(model); engine.apply_combinations(model)
    result = engine.analyze_and_design(model, {"synthetic_test_data": True})
    drawing = DrawingProductionAdapter().produce(graph, result, tmp_path / "drawing")
    quantities = QuantityWorkbookAdapter().produce(graph, tmp_path / "quantities")
    reports = ReportProductionAdapter().produce(graph, result, drawing["model"], quantities["package"], tmp_path / "reports")
    qa = ProfessionalQAAdapter().evaluate(result, drawing, quantities, reports, "NOMINAL_CASE_001")
    issuance = ExecutiveIssuanceAdapter().issue("NOMINAL_CASE_001", tmp_path, drawing, quantities, reports, qa)
    assert set(quantities["element_ids"]) <= {node["id"] for node in graph.nodes}
    assert issuance["gate"] == qa["gate"] == drawing["gate"] == "PASS"
