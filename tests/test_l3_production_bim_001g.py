"""Focused regression for L3-PRODUCTION-BIM-001G."""
from pathlib import Path

import pytest

from aias_l3_production_bim.exact_documentation_service import (
    ExactNativeDocumentationProjectService,
)


def _discovery() -> Path:
    return Path("AIAS_L3_PRODUCTION_BIM_DISCOVERY_CURRENT") / "DISCOVERY.json"


def _service():
    service = ExactNativeDocumentationProjectService(
        "001G Test",
        discovery_path=_discovery(),
    )
    service.start()
    return service


def test_001g_exact_documentation_view_and_sheet_creation():
    service = _service()
    level = service.add_level("Level 1", 0.0)
    view = service.add_documentation_plan_view(
        "Level 1 Plan",
        level.id,
        scale=100.0,
    )
    sheet = service.add_documentation_sheet(
        "A101",
        "Level 1 Plan",
        width=841.0,
        height=594.0,
    )

    snap = service.professional_documentation_snapshot()
    assert view.id in service.documentation.views
    assert service.documentation.sheet_manager.get(sheet.id).sheet_id == sheet.id
    assert snap["native_views"] == 1
    assert snap["native_sheets"] == 1


def test_001g_places_exact_native_viewport_and_canonical_view():
    service = _service()
    level = service.add_level("Level 1", 0.0)
    view = service.add_documentation_plan_view(
        "Level 1 Plan",
        level.id,
        scale=100.0,
    )
    sheet = service.add_documentation_sheet(
        "A101",
        "Level 1",
        width=841.0,
        height=594.0,
    )
    viewport_id = service.place_documentation_view_on_sheet(
        sheet.id,
        view.id,
        x=50.0,
        y=50.0,
        width=300.0,
        height=200.0,
    )

    native_sheet = service.documentation.sheet_manager.get(sheet.id)
    assert viewport_id
    assert view.id in service.state.sheets[sheet.id].view_ids
    assert len(native_sheet.viewports) == 1
    assert native_sheet.viewports[0].view_id == view.id


def test_001g_native_sheet_manager_rejects_overlapping_viewports():
    service = _service()
    level = service.add_level("Level 1", 0.0)
    view1 = service.add_documentation_plan_view("Plan A", level.id, scale=100.0)
    view2 = service.add_documentation_plan_view("Plan B", level.id, scale=50.0)
    sheet = service.add_documentation_sheet(
        "A101",
        "Plans",
        width=841.0,
        height=594.0,
    )

    service.place_documentation_view_on_sheet(
        sheet.id,
        view1.id,
        x=10.0,
        y=10.0,
        width=200.0,
        height=150.0,
    )

    with pytest.raises(ValueError):
        service.place_documentation_view_on_sheet(
            sheet.id,
            view2.id,
            x=100.0,
            y=50.0,
            width=200.0,
            height=150.0,
        )

    # Canonical placement of the rejected second view must not occur.
    assert view2.id not in service.state.sheets[sheet.id].view_ids


def test_001g_show_sheet_uses_audited_drawing_viewer_contract():
    calls = []

    class Viewer:
        def show_sheet(self, sheet):
            calls.append(sheet)
            return sheet.sheet_id

    service = ExactNativeDocumentationProjectService(
        "001G Viewer",
        discovery_path=_discovery(),
        drawing_viewer=Viewer(),
    )
    service.start()
    sheet = service.add_documentation_sheet(
        "A001",
        "Cover",
        width=841.0,
        height=594.0,
    )

    result = service.show_documentation_sheet(sheet.id)
    assert result == sheet.id
    assert calls[0].sheet_id == sheet.id


def test_001g_exact_native_report_marks_all_four_domains():
    service = _service()
    report = service.exact_native_report()
    assert report["exact_native_domains"] == [
        "levels",
        "grids",
        "views",
        "documentation",
    ]
