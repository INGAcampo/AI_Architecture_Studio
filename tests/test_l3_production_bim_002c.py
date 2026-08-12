"""Focused regression for L3-PRODUCTION-BIM-002C."""
from pathlib import Path
from types import SimpleNamespace

from documentation_kernel.model import AnnotationKind

from aias_l3_production_bim.professional_documentation_service import (
    ProfessionalDocumentationProjectService,
)


def _discovery() -> Path:
    return Path("AIAS_L3_PRODUCTION_BIM_DISCOVERY_CURRENT") / "DISCOVERY.json"


def _service():
    service = ProfessionalDocumentationProjectService(
        "002C Test",
        discovery_path=_discovery(),
    )
    service.start()
    return service


def test_002c_plan_view_is_registered_in_professional_view_manager():
    service = _service()
    level = service.add_level("Level 1", 0.0)
    view = service.add_documentation_plan_view(
        "Level 1 Plan",
        level.id,
        scale=100.0,
    )
    assert service.professional.views.get(view.id).view_id == view.id


def test_002c_section_and_elevation_use_native_generator():
    service = _service()
    level = service.add_level("Level 1", 0.0)

    # The native section/elevation kernel contract requires attribute-based
    # elements exposing element_id and coordinates.
    elements = [
        SimpleNamespace(
            element_id="E1",
            x=0.0,
            y=0.0,
            z=0.0,
            width=1.0,
            height=3.0,
        ),
        SimpleNamespace(
            element_id="E2",
            x=5.0,
            y=0.0,
            z=3.0,
            width=1.0,
            height=3.0,
        ),
    ]

    section = service.generate_section_view(
        "Section A-A",
        elements=elements,
        cut_x=2.5,
        depth=10.0,
        scale=50.0,
        level_id=level.id,
    )
    elevation = service.generate_elevation_view(
        "North Elevation",
        elements=elements,
        direction="north",
        scale=50.0,
        level_id=level.id,
    )

    assert section.id in service.professional.generated_views
    assert elevation.id in service.professional.generated_views


def test_002c_dimensions_annotations_and_workspace_projection():
    service = _service()
    level = service.add_level("Level 1", 0.0)
    view = service.add_documentation_plan_view(
        "Level 1 Plan",
        level.id,
        scale=100.0,
    )

    dimension = service.add_view_dimension(
        view.id,
        dimension_id="D1",
        start=(0.0, 0.0),
        end=(5.0, 0.0),
        suffix=" m",
        precision=2,
    )
    annotation = service.add_view_annotation(
        view.id,
        annotation_id="A1",
        kind=AnnotationKind.TEXT,
        text="Entry",
        x=1.0,
        y=1.0,
    )

    projection = service.workspace_projection_with_professional_docs()
    assert dimension.formatted()
    assert annotation.annotation_id == "A1"
    assert "D1" in projection["professional_documentation"]["dimension_ids"]
    assert projection["professional_documentation"]["annotations"] == 1


def test_002c_intelligent_tag_and_schedule():
    service = _service()

    tag = service.render_element_tag(
        element_id="ROOM-101",
        properties={"number": "101", "name": "Lobby"},
        template_id="ROOM-TAG",
        pattern="{number} - {name}",
    )

    elements = [
        {"number": "101", "name": "Lobby", "area": 25.0},
        {"number": "102", "name": "Office", "area": 15.0},
    ]
    schedule = service.build_project_schedule(
        schedule_id="ROOM-SCHEDULE",
        elements=elements,
        columns=(
            ("number", "Number"),
            ("name", "Name"),
            ("area", "Area"),
        ),
        sort_key=lambda item: item["number"],
    )

    assert tag
    assert schedule.schedule_id == "ROOM-SCHEDULE"
    assert len(schedule.rows) == 2
