"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
from pathlib import Path

from aias_omega_core.materials import Material
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.persistence import ProjectSerializer
from aias_omega_core.project import EngineeringProject

from .adapters import CadToBimAdapter, WallType
from .quantity import QuantityEngine
from .reports import EngineeringReportService
from .structural import StructuralAdapter
from .validation import ProjectValidator

def build_operational_project() -> EngineeringProject:
    """Build the operational project required by the second Omega integrated product release from explicit inputs."""
    project = EngineeringProject("Omega Operational Demo")

    project.materials.add(Material(
        "CONC_30",
        "Concrete 30 MPa",
        "concrete",
        {
            "E_MPa": 30000.0,
            "density_kg_m3": 2400.0,
        },
    ))

    cad_axis = EngineeringObject(
        object_type="cad_line",
        name="Wall Axis W01",
        geometry={
            "type": "line",
            "start": [0.0, 0.0],
            "end": [6.0, 0.0],
        },
        classification="CAD.Axis",
    )
    cad_id = project.add_object(cad_axis)

    wall_id = CadToBimAdapter().line_to_wall(
        project,
        cad_id,
        WallType(
            name="Concrete Wall 200",
            thickness_m=0.20,
            height_m=3.20,
            material_id="CONC_30",
        ),
        wall_name="Wall W01",
    )

    StructuralAdapter().wall_to_analytical_bar(
        project,
        wall_id,
        tributary_width_m=1.0,
        load_n=120_000.0,
    )

    QuantityEngine().attach_wall_quantity(
        project,
        wall_id,
        unit_cost_per_m3=185.0,
    )

    issues = ProjectValidator().validate(project)
    if issues:
        raise RuntimeError(f"Workflow produced validation issues: {issues}")

    return project

def save_operational_outputs(output_directory: Path) -> dict[str, Path]:
    """Persist operational outputs for the second Omega integrated product release in its stable external representation."""
    output_directory.mkdir(parents=True, exist_ok=True)
    project = build_operational_project()

    project_path = output_directory / "omega_release_2_project.aias.json"
    report_json = output_directory / "omega_release_2_report.json"
    report_csv = output_directory / "omega_release_2_objects.csv"
    report_md = output_directory / "omega_release_2_report.md"

    ProjectSerializer().save(project, project_path)
    service = EngineeringReportService()
    service.export_json(project, report_json)
    service.export_objects_csv(project, report_csv)
    report_md.write_text(service.markdown(project), encoding="utf-8")

    return {
        "project": project_path,
        "report_json": report_json,
        "report_csv": report_csv,
        "report_md": report_md,
    }
