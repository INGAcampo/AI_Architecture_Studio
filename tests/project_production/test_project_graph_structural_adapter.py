from aias_project_intake.builders import ParametricProjectGraphBuilder
from aias_project_production.orchestrator import AIASProjectProductionOrchestrator
from aias_project_production.adapters import NativeDWGProductionAdapter
from aias_project_production.certification import certify_structural_production_core
from aias_structural_professional import ProfessionalStructuralEngine
import json


def _manifest(project_id: str, width: float = 8.0):
    return {
        "project_id": project_id, "project_name": project_id,
        "mode": "PILOT_SYNTHETIC", "scenario_id": "NOMINAL_CASE_001",
        "SYNTHETIC_TEST_DATA": True, "NOT_FOR_CONSTRUCTION": True,
        "building_program": {"levels": 2, "width_m": width, "length_m": 9.0, "storey_height_m": 3.0},
    }


def test_parametric_graph_projects_geometry_backed_structural_connectivity():
    graph = ParametricProjectGraphBuilder().build(_manifest("STRUCT-CONNECT"))
    model = ProfessionalStructuralEngine().generate_3d_model(graph)

    assert model.metadata["projection"] == "aias.project_graph_structural_adapter.v1"
    assert model.metadata["geometry_backed_member_count"] == len(model.members)
    assert all(len(member["node_ids"]) == 2 for member in model.members)
    assert all(node["geometry_status"] == "PROJECT_GRAPH_GEOMETRY" for node in model.nodes)
    beam = next(member for member in model.members if member["id"] == "beam-01-1")
    coordinates = {node["id"]: node["xyz_m"] for node in model.nodes}
    assert coordinates[beam["node_ids"][0]] == [0.0, 0.0, 3.0]
    assert coordinates[beam["node_ids"][1]] == [8.0, 0.0, 3.0]
    assert all(any(node["support"] for node in model.nodes if node["id"] in member["node_ids"]) for member in model.members if member["type"] == "foundation")


def test_structural_projection_is_project_isolated_and_geometry_sensitive():
    engine = ProfessionalStructuralEngine()
    first = engine.generate_3d_model(ParametricProjectGraphBuilder().build(_manifest("STRUCT-A", 8.0)))
    second = engine.generate_3d_model(ParametricProjectGraphBuilder().build(_manifest("STRUCT-B", 11.0)))

    assert first.project_id != second.project_id
    assert first.metadata["source_graph_sha256"] != second.metadata["source_graph_sha256"]
    first_beam = next(member for member in first.members if member["id"] == "beam-01-1")
    second_beam = next(member for member in second.members if member["id"] == "beam-01-1")
    lookup = lambda model, node_id: next(node["xyz_m"] for node in model.nodes if node["id"] == node_id)
    assert lookup(first, first_beam["node_ids"][1]) != lookup(second, second_beam["node_ids"][1])


def test_orchestrator_emits_traceable_structural_evidence(tmp_path, monkeypatch):
    monkeypatch.setattr(NativeDWGProductionAdapter, "produce", lambda self, cad, output: {
        "gate": "V5_NATIVE_DWG_INTEGRATION_PASS", "backend": "TEST", "drawings": [], "sha256": "0" * 64,
    })
    result = AIASProjectProductionOrchestrator(tmp_path).run(
        "NOMINAL_CASE_001", project_id="STRUCT-EVIDENCE", manifest=_manifest("STRUCT-EVIDENCE")
    )
    evidence_path = result["structural"]["path"]
    evidence = json.loads(open(evidence_path, encoding="utf-8").read())
    assert result["structural"]["projection"] == "aias.project_graph_structural_adapter.v1"
    assert result["structural"]["geometry_backed_member_count"] == result["structural"]["member_count"]
    assert evidence["source_graph_sha256"] == result["architecture"]["source_graph_sha256"]


def test_structural_certification_proves_two_isolated_geometry_backed_projects(tmp_path):
    certification = certify_structural_production_core(tmp_path)
    assert certification["verdict"] == "STRUCTURAL_PRODUCTION_CORE_READY"
    assert all(certification["checks"].values())
    assert {project["project_id"] for project in certification["projects"]} == {
        "STRUCT-CORE-CERT-A", "STRUCT-CORE-CERT-B"
    }
