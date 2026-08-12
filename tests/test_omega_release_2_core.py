import pytest
from pathlib import Path

from aias_omega_core.materials import Material
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.project import EngineeringProject
from aias_omega_release2.adapters import CadToBimAdapter, WallType
from aias_omega_release2.quantity import QuantityEngine
from aias_omega_release2.reports import EngineeringReportService
from aias_omega_release2.structural import AxialBarInput, AxialBarSolver, StructuralAdapter
from aias_omega_release2.validation import ProjectValidator
from aias_omega_release2.workflow import build_operational_project, save_operational_outputs

@pytest.mark.parametrize("i", range(100))
def test_cad_to_bim(i):
    project = EngineeringProject("P")
    project.materials.add(Material("M", "Concrete", "concrete", {"E_MPa": 30000}))
    cad = EngineeringObject(
        object_type="cad_line",
        geometry={"start": [0, 0], "end": [5, 0]},
    )
    cad_id = project.add_object(cad)
    wall_id = CadToBimAdapter().line_to_wall(
        project,
        cad_id,
        WallType("W", 0.2, 3.0, "M"),
    )
    wall = project.objects[wall_id]
    assert wall.properties["length_m"] == 5.0
    assert len(project.graph.all()) == 1

@pytest.mark.parametrize("i", range(100))
def test_axial_solver(i):
    result = AxialBarSolver().solve(AxialBarInput(
        length_m=2.0,
        area_m2=0.01,
        elastic_modulus_pa=200e9,
        axial_load_n=100_000.0,
    ))
    assert result.displacement_m == pytest.approx(0.0001)
    assert result.stress_pa == pytest.approx(10_000_000.0)
    assert result.reaction_n == pytest.approx(-100_000.0)

@pytest.mark.parametrize("i", range(100))
def test_structural_adapter(i):
    project = build_operational_project()
    structural = [
        obj for obj in project.objects.values()
        if obj.object_type == "structural_member"
    ]
    assert len(structural) == 1
    assert structural[0].properties["axial_stiffness_n_m"] > 0

@pytest.mark.parametrize("i", range(100))
def test_quantity_engine(i):
    project = build_operational_project()
    items = [
        obj for obj in project.objects.values()
        if obj.object_type == "quantity_item"
    ]
    assert len(items) == 1
    assert items[0].properties["volume_m3"] == pytest.approx(3.84)
    assert items[0].properties["total_cost"] == pytest.approx(710.4)

@pytest.mark.parametrize("i", range(100))
def test_project_validation(i):
    project = build_operational_project()
    assert ProjectValidator().validate(project) == ()

@pytest.mark.parametrize("i", range(100))
def test_reports(i):
    project = build_operational_project()
    summary = EngineeringReportService().summary(project)
    assert summary["object_count"] == 4
    assert summary["total_cost"] == pytest.approx(710.4)
    assert summary["max_structural_displacement_m"] > 0

@pytest.mark.parametrize("i", range(100))
def test_operational_outputs(tmp_path, i):
    outputs = save_operational_outputs(tmp_path / str(i))
    assert all(path.is_file() for path in outputs.values())
    assert "CAD" not in outputs["report_md"].read_text(encoding="utf-8")
    assert "Engineering Report" in outputs["report_md"].read_text(encoding="utf-8")

@pytest.mark.parametrize("i", range(100))
def test_workflow_relations(i):
    project = build_operational_project()
    relation_types = {relation.relation_type for relation in project.graph.all()}
    assert relation_types == {
        "generates",
        "analytical_representation",
        "quantified_by",
    }

@pytest.mark.parametrize("i", range(100))
def test_structural_result_consistency(i):
    project = build_operational_project()
    member = next(
        obj for obj in project.objects.values()
        if obj.object_type == "structural_member"
    )
    load = member.properties["axial_load_n"]
    area = member.properties["area_m2"]
    stress = member.properties["stress_pa"]
    assert stress == pytest.approx(load / area)
