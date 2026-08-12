"""Focused regression for L3-PRODUCTION-BIM-001I."""
from pathlib import Path

from aias_l3_production_bim.exact_persistent_service import (
    ExactNativePersistentProjectService,
)


def _discovery() -> Path:
    return Path("AIAS_L3_PRODUCTION_BIM_DISCOVERY_CURRENT") / "DISCOVERY.json"


def _project():
    service = ExactNativePersistentProjectService(
        "001I Test",
        discovery_path=_discovery(),
    )
    service.start()
    level = service.add_level("Level 1", 0.0)
    service.add_grid("A", (0.0, 0.0), (10.0, 0.0))
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
    vp = service.place_documentation_view_on_sheet(
        sheet.id,
        view.id,
        x=50.0,
        y=40.0,
        width=300.0,
        height=200.0,
    )
    return service, level, view, sheet, vp


def test_001i_viewport_geometry_is_canonical_and_persistable():
    service, _, view, sheet, vp = _project()
    layout = service.state.sheets[sheet.id].properties["native_viewports"]

    assert layout == [
        {
            "viewport_id": vp,
            "view_id": view.id,
            "x": 50.0,
            "y": 40.0,
            "width": 300.0,
            "height": 200.0,
        }
    ]


def test_001i_rebuilds_all_exact_native_domains_from_canonical_state():
    service, level, view, sheet, vp = _project()

    # Destroy transient native state, then prove deterministic rehydration.
    service.level_grid.levels.clear()
    service.level_grid.grids.clear()
    service.documentation.views.clear()
    service.documentation = type(service.documentation)()

    report = service.rebuild_exact_native_state()

    assert level.id in service.level_grid.levels
    assert view.id in service.documentation.views
    native_sheet = service.documentation.sheet_manager.get(sheet.id)
    assert native_sheet.viewports[0].viewport_id == vp
    assert report["exact_native_domains"][:4] == [
        "levels",
        "grids",
        "views",
        "documentation",
    ]


def test_001i_workspace_projection_contains_exact_native_documentation():
    service, _, view, sheet, vp = _project()
    projection = service.workspace_projection_with_native_docs()

    exact = projection["exact_native_documentation"]
    assert view.id in exact["views"]
    assert exact["sheets"][0]["sheet_id"] == sheet.id
    assert exact["sheets"][0]["viewports"][0]["viewport_id"] == vp
    assert "workspace2" in projection["exact_native_domains"]
