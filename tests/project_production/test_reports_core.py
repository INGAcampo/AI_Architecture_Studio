from aias_building_design_core import BuildingDesignCore
from aias_standards_core import StandardsPack
from aias_structural_core import StructuralAnalysisCore
from aias_drawing_core import DrawingCore
from aias_quantities_core import QuantityTakeoffEngine
from aias_reports_core import ReportCore

def test_report_package_is_traceable(tmp_path):
    graph = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot"))
    sc = StructuralAnalysisCore(); model = sc.generate_model(graph); sc.add_load_case(model, "dead", 100); sc.apply_ve_combinations(model)
    result = sc.solve_linear(model, {"source": "VE-PILOT-001.0"})
    drawing = DrawingCore().build(graph, {"status": result.status}); quantities = QuantityTakeoffEngine().build(graph)
    package = ReportCore().build(graph, StandardsPack(), result, drawing, quantities)
    assert {"memoria_descriptiva", "memoria_calculo_v0", "reporte_normativo"} <= package.documents.keys()
    exported = ReportCore().export(package, tmp_path)
    assert len(exported) >= 8 and all(len(value) == 64 for value in exported.values())

def test_report_fail_closed_without_analysis():
    graph = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot"))
    try: ReportCore().build(graph, StandardsPack(), None, None, None)
    except ValueError as exc: assert "insufficient" in str(exc)
    else: raise AssertionError("expected fail-closed report generation")
