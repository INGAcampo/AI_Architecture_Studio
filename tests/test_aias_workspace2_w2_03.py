from dataclasses import dataclass

import pytest

from gui.project_browser import ProjectBrowserBuilder, ProjectBrowserController
from gui.property_palette import PropertyPaletteController, PropertyPaletteModel, PropertySchemaRegistry, PropertySelectionAdapter, default_wall_schema
from gui.workspace import WorkspaceManager
from gui.workspace2 import BimInspectorCoordinator


@dataclass
class Wall:
    object_id: str
    name: str
    height: float
    thickness: float = 0.2
    base_elevation: float = 0.0
    length: float = 4.0
    area: float = 12.0
    volume: float = 2.4
    ifc_class: str = "IfcWall"
    object_type: str = "wall"
    category: str = "Walls"
    level_name: str = "Level 1"
    materials: tuple = ()


def build(tmp_path):
    walls = (Wall("w1", "Wall 1", 3.0), Wall("w2", "Wall 2", 3.2))
    workspace = WorkspaceManager(tmp_path / "layouts")
    browser = ProjectBrowserController(ProjectBrowserBuilder().build(walls))
    schemas = PropertySchemaRegistry(); schemas.register("wall", default_wall_schema())
    properties = PropertyPaletteController(PropertyPaletteModel(), PropertySelectionAdapter(schemas))
    return walls, workspace, browser, properties, BimInspectorCoordinator(workspace, browser, properties, walls)


def test_browser_canvas_and_properties_share_one_selection(tmp_path):
    walls, workspace, browser, properties, coordinator = build(tmp_path)
    result = coordinator.select_from_browser("object.w1")
    assert result["resolved"] == 1
    assert workspace.state.selection_ids == ("w1",)
    assert properties.selection == (walls[0],)
    assert properties.model.require("height").value == 3.0
    coordinator.select_from_canvas(["w2"])
    assert browser.state.selected_node_id == "object.w2"
    assert properties.selection == (walls[1],)


def test_group_and_missing_selection_do_not_fabricate_properties(tmp_path):
    _, workspace, _, properties, coordinator = build(tmp_path)
    coordinator.select_from_browser("group.levels")
    assert workspace.state.selection_ids == () and properties.selection == ()
    result = coordinator.select_from_canvas(["deleted-object"])
    assert result["missing"] == ["deleted-object"]
    assert workspace.state.selection_ids == ("deleted-object",)
    assert properties.selection == ()


def test_standard_panels_are_idempotent_and_recoverable(tmp_path):
    _, workspace, _, _, coordinator = build(tmp_path)
    coordinator.install_standard_panels(); coordinator.install_standard_panels()
    assert {item.panel_id for item in workspace.registry.all()} == {"project_browser", "property_inspector"}
    assert workspace.state.panels["project_browser"].area.value == "left"
    assert workspace.state.panels["property_inspector"].area.value == "right"


def test_duplicate_or_unstable_object_ids_fail_closed(tmp_path):
    walls, _, _, _, coordinator = build(tmp_path)
    with pytest.raises(KeyError, match="duplicate"):
        coordinator.refresh_objects((walls[0], walls[0]))
    with pytest.raises(ValueError, match="stable_id"):
        coordinator.refresh_objects(({"name": "No id"},))
