"""Focused regression for L3-PRODUCTION-BIM-001F."""
from pathlib import Path

from aias_l3_production_bim.exact_native_service import ExactNativeProjectAuthoringService
from aias_l3_production_bim.native_level_grid import NativeLevelGridBridge


def _discovery() -> Path:
    return Path("AIAS_L3_PRODUCTION_BIM_DISCOVERY_CURRENT") / "DISCOVERY.json"


def test_001f_native_level_grid_contract_preflight():
    """The audited repository must expose usable native Level/Grid model contracts."""
    bridge = NativeLevelGridBridge()
    report = bridge.report()
    assert report["level_model"]
    assert report["grid_model"]
    assert report["native_levels"] == 0
    assert report["native_grids"] == 0


def test_001f_level_is_registered_and_converted_natively():
    """A canonical project level must have a native manager object and BIM element."""
    service = ExactNativeProjectAuthoringService(
        "001F Level Test",
        discovery_path=_discovery(),
    )
    service.start()
    level = service.add_level("Level 1", 0.0)
    mirror = service.level_grid.levels[level.id]

    assert level.id in service.state.levels
    assert service.level_grid.level_manager.get_levels()
    assert mirror.bim_element is not None
    assert service.level_grid.level_adapter.supports(mirror.native_source)


def test_001f_grid_is_registered_and_converted_natively():
    """A canonical project grid must have a native manager object and BIM element."""
    service = ExactNativeProjectAuthoringService(
        "001F Grid Test",
        discovery_path=_discovery(),
    )
    service.start()
    grid = service.add_grid("A", (0.0, 0.0), (0.0, 10.0))
    mirror = service.level_grid.grids[grid.id]

    assert grid.id in service.state.grids
    assert service.level_grid.grid_manager.get_grids()
    assert mirror.bim_element is not None
    assert service.level_grid.grid_adapter.supports(mirror.native_source)


def test_001f_level_and_grid_remain_available_to_project_workflow():
    """Native activation must not remove certified 001B project authoring behavior."""
    service = ExactNativeProjectAuthoringService(
        "001F Workflow",
        discovery_path=_discovery(),
    )
    service.start()
    level = service.add_level("Level 1", 0.0)
    grid = service.add_grid("A", (0, 0), (10, 0))
    view = service.add_plan_view("Level 1 Plan", level.id)
    sheet = service.add_sheet("A101", "Level 1", [view.id])

    assert level.id in service.state.levels
    assert grid.id in service.state.grids
    assert view.id in service.state.views
    assert sheet.id in service.state.sheets
