import copy
import hashlib
import json
from pathlib import Path

import pytest

from aias_building_design_core import ArchitecturalProductionCore
from aias_building_design_core import NativeBimProjection
from aias_drawing_core import DrawingCore
from aias_project_intake.builders import ParametricProjectGraphBuilder
from aias_project_production.adapters import NativeDWGProductionAdapter
from aias_project_production.certification import certify_architectural_production_core
from aias_project_production.factory import ProjectProductionFactory
from aias_project_production.orchestrator import AIASProjectProductionOrchestrator
from aias_quantities_core import QuantityTakeoffEngine
from aias_structural_core import StructuralAnalysisCore


def manifest(project_id, width=8.0, length=9.0, levels=2):
    return {
        "project_id": project_id,
        "project_name": f"Synthetic {project_id}",
        "mode": "PILOT_SYNTHETIC",
        "scenario_id": "NOMINAL_CASE_001",
        "SYNTHETIC_TEST_DATA": True,
        "NOT_FOR_CONSTRUCTION": True,
        "building_program": {
            "levels": levels,
            "width_m": width,
            "length_m": length,
            "storey_height_m": 3.0,
        },
    }


def graph_node(graph, node_id):
    return next(node for node in graph.nodes if node["id"] == node_id)


def test_architectural_core_materializes_complete_spatial_contract():
    graph = ParametricProjectGraphBuilder().build(manifest("ARCH-SPATIAL"))
    core = ArchitecturalProductionCore()

    assert core.validate(graph) == []
    architecture = core.materialize(graph)

    assert architecture["schema"] == "aias.architectural_production_core.v1"
    assert len(architecture["levels"]) == 2
    assert len(architecture["grids"]) == 4
    assert len(architecture["envelope"]["wall_ids"]) == 8
    assert architecture["envelope"]["net_wall_area_m2"] < architecture["envelope"]["gross_wall_area_m2"]
    assert set(architecture["openings"]) == {
        "door-01-01", "window-01-01", "door-02-01", "window-02-01"
    }
    assert all(item["geometry_sha256"] for item in architecture["geometry_index"].values())


def test_coherence_binds_bim_analysis_drawings_and_quantities_to_one_graph():
    graph = ParametricProjectGraphBuilder().build(manifest("ARCH-COHERENCE"))
    core = ArchitecturalProductionCore()
    architecture = core.materialize(graph)
    analysis = StructuralAnalysisCore().generate_model(graph)
    drawings = DrawingCore().build(graph, {"status": "PASS"})
    quantities = QuantityTakeoffEngine().build(graph)
    native_bim = NativeBimProjection().materialize(graph)

    coherence = core.verify_coherence(
        graph, architecture, analysis, drawings, quantities, native_bim=native_bim
    )

    assert coherence["verdict"] == "ARCHITECTURAL_PIPELINE_COHERENT"
    assert all(coherence["checks"].values())
    wall = graph_node(graph, "wall-01-south")
    gross_volume = wall["properties"]["length_m"] * wall["properties"]["height_m"] * wall["properties"]["thickness_m"]
    wall_quantity = next(item for item in quantities.items if item["element_id"] == wall["id"])
    assert wall_quantity["measurement"] < gross_volume


def test_architectural_validation_rejects_invalid_hosted_opening_geometry():
    graph = ParametricProjectGraphBuilder().build(manifest("ARCH-INVALID-OPENING"))
    opening = graph_node(graph, "window-01-01")
    opening["properties"]["sill_height_m"] = 2.5
    opening["properties"]["geometry"]["host_wall_id"] = "wall-01-south"

    errors = ArchitecturalProductionCore().validate(graph)

    assert "window-01-01 exceeds its host wall height" in errors
    assert "window-01-01 geometry host does not match relationship host" in errors


def test_opening_change_selectively_preserves_structural_analysis():
    builder = ParametricProjectGraphBuilder()
    before = builder.build(manifest("ARCH-REGEN"))
    after = copy.deepcopy(before)
    graph_node(after, "window-01-01")["properties"]["offset_m"] += 0.25
    graph_node(after, "window-01-01")["properties"]["geometry"]["offset_m"] += 0.25

    plan = ArchitecturalProductionCore().plan_selective_regeneration(before, after)

    assert plan["project_id"] == "ARCH-REGEN"
    assert plan["changed_node_ids"] == ["window-01-01"]
    assert "drawings" in plan["order"] and "quantities" in plan["order"]
    assert "analysis" in plan["preserved"]
    with pytest.raises(ValueError, match="cross project"):
        ArchitecturalProductionCore().plan_selective_regeneration(
            before, builder.build(manifest("OTHER-PROJECT"))
        )


def test_factory_runs_two_isolated_projects_through_same_architectural_core(tmp_path, monkeypatch):
    monkeypatch.setattr(
        NativeDWGProductionAdapter,
        "produce",
        lambda self, cad, output: {
            "gate": "V5_NATIVE_DWG_INTEGRATION_PASS",
            "backend": "SYNTHETIC_TEST_DOUBLE",
            "drawings": [],
            "sha256": "0" * 64,
        },
    )
    manifests = [
        manifest("ARCH-CERT-A", width=8.0, length=9.0),
        manifest("ARCH-CERT-B", width=11.0, length=7.0, levels=3),
    ]

    result = ProjectProductionFactory(tmp_path).run(manifests)

    assert result["verdict"] == "PROJECT_PRODUCTION_FACTORY_READY"
    assert result["isolation_verified"] is True
    assert len(result["new_results"]) == 2
    providers = {item["architecture"]["provider"] for item in result["new_results"]}
    graph_hashes = {item["architecture"]["source_graph_sha256"] for item in result["new_results"]}
    assert providers == {"aias_building_design_core.ArchitecturalProductionCore"}
    assert len(graph_hashes) == 2
    assert all(item["coherence"]["verdict"] == "ARCHITECTURAL_PIPELINE_COHERENT" for item in result["new_results"])
    for item in result["new_results"]:
        architecture_path = Path(item["architecture"]["path"])
        assert architecture_path.is_relative_to(tmp_path / "runtime" / "projects" / item["project_id"])
        assert json.loads(architecture_path.read_text(encoding="utf-8"))["project_id"] == item["project_id"]

    updated = copy.deepcopy(manifests[0])
    updated["building_program"]["width_m"] = 10.0
    regeneration = ProjectProductionFactory(tmp_path).plan_selective_regeneration("ARCH-CERT-A", updated)
    assert regeneration["project_id"] == "ARCH-CERT-A"
    assert "analysis" in regeneration["order"]
    assert (tmp_path / "runtime/projects/ARCH-CERT-A/manifests/SELECTIVE_REGENERATION_PLAN.json").exists()
    assert not (tmp_path / "runtime/projects/ARCH-CERT-B/manifests/SELECTIVE_REGENERATION_PLAN.json").exists()


def test_real_project_without_authenticated_baseline_fails_closed(tmp_path):
    with pytest.raises(ValueError, match="AUTHENTICATED_EXTERNAL_INPUT_REQUIRED"):
        AIASProjectProductionOrchestrator(tmp_path).run(
            "NOMINAL_CASE_001", project_id="REAL-001", mode="REAL_PROJECT"
        )


def test_committed_certification_evidence_has_two_isolated_synthetic_projects():
    repository = Path(__file__).resolve().parents[2]
    certification = repository / "engineering/aias/architectural_core_certification"
    record = json.loads(
        (certification / "ARCHITECTURAL_PRODUCTION_CORE_MANIFEST.json").read_text(encoding="utf-8")
    )

    assert record["verdict"] == "ARCHITECTURAL_PRODUCTION_CORE_READY"
    assert record["SYNTHETIC_TEST_DATA"] is record["NOT_FOR_CONSTRUCTION"] is True
    assert record["same_core_verified"] is record["isolation_verified"] is True
    assert len(record["projects"]) == 2
    assert len({project["source_graph_sha256"] for project in record["projects"]}) == 2
    artifact_names = {
        "project_graph": "project_graph.json",
        "architecture": "architectural_model.json",
        "native_bim": "native_bim_projection.json",
        "coherence": "pipeline_coherence.json",
    }
    for project in record["projects"]:
        root = repository / project["artifact_root"]
        assert all(project["coherence_checks"].values())
        for evidence_type, filename in artifact_names.items():
            digest = hashlib.sha256((root / filename).read_bytes()).hexdigest()
            assert digest == project["artifact_sha256"][evidence_type]


def test_certification_publishes_two_compact_isolated_project_evidence_files(tmp_path):
    result = certify_architectural_production_core(tmp_path)

    assert result["verdict"] == "ARCHITECTURAL_PRODUCTION_CORE_READY"
    assert all(result["checks"].values())
    assert {item["project_id"] for item in result["projects"]} == {
        "ARCH-CORE-CERT-A", "ARCH-CORE-CERT-B"
    }
    assert (tmp_path / "ARCHITECTURAL_PRODUCTION_CORE_MANIFEST.json").exists()
    assert all((tmp_path / item["evidence_file"]).exists() for item in result["projects"])
