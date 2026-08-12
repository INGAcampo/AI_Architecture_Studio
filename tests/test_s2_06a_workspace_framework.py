import json

import pytest

from gui.workspace import (
    DockArea,
    DocumentSession,
    LayoutManager,
    PanelDescriptor,
    PanelRegistry,
    WorkspaceManager,
    WorkspaceSerializer,
    WorkspaceState,
)


def manager(tmp_path, events=None, graph=None):
    return WorkspaceManager(tmp_path / "layouts", event_dispatcher=events, graph=graph)


def test_panel_descriptor_validation():
    with pytest.raises(ValueError):
        PanelDescriptor("", "Panel")
    with pytest.raises(ValueError):
        PanelDescriptor("panel", "")


def test_registry_register_and_get():
    registry = PanelRegistry()
    descriptor = PanelDescriptor("properties", "Propiedades")
    registry.register(descriptor)
    assert registry.get("properties") is descriptor


def test_registry_rejects_duplicate():
    registry = PanelRegistry()
    registry.register(PanelDescriptor("p", "P"))
    with pytest.raises(KeyError):
        registry.register(PanelDescriptor("p", "Otro"))


def test_panel_activation_uses_default_area(tmp_path):
    workspace = manager(tmp_path)
    workspace.register_panel(PanelDescriptor("project", "Proyecto", DockArea.LEFT))
    state = workspace.panels.activate("project")
    assert state.area is DockArea.LEFT
    assert state.visible


def test_hide_and_show_panel(tmp_path):
    workspace = manager(tmp_path)
    workspace.register_panel(PanelDescriptor("output", "Salida"))
    workspace.panels.activate("output")
    assert not workspace.panels.hide("output").visible
    assert workspace.panels.show("output").visible


def test_dock_panel(tmp_path):
    workspace = manager(tmp_path)
    workspace.register_panel(PanelDescriptor("layers", "Capas"))
    state = workspace.docks.dock("layers", DockArea.LEFT, order=2)
    assert state.area is DockArea.LEFT
    assert state.order == 2
    assert not state.floating


def test_float_panel_validates_geometry(tmp_path):
    workspace = manager(tmp_path)
    workspace.register_panel(PanelDescriptor("history", "Historial"))
    with pytest.raises(ValueError):
        workspace.docks.float("history", (0, 0, 0, 200))
    state = workspace.docks.float("history", (10, 20, 400, 300))
    assert state.floating
    assert state.geometry == (10, 20, 400, 300)


def test_auto_hide(tmp_path):
    workspace = manager(tmp_path)
    workspace.register_panel(PanelDescriptor("ai", "AI"))
    assert workspace.docks.set_auto_hide("ai", True).auto_hide


def test_open_document_becomes_active(tmp_path):
    workspace = manager(tmp_path)
    document = workspace.open_document("C:/modelos/casa.aias")
    assert workspace.active_document is document
    assert document.title == "casa"


def test_multiple_documents_and_activation(tmp_path):
    workspace = manager(tmp_path)
    first = workspace.open_document(title="A")
    second = workspace.open_document(title="B")
    workspace.activate_document(first.document_id)
    assert workspace.active_document is first
    assert len(workspace.state.documents) == 2
    assert second.document_id in workspace.state.documents


def test_modified_document_requires_force_to_close(tmp_path):
    workspace = manager(tmp_path)
    document = workspace.open_document(title="A")
    document.mark_modified()
    with pytest.raises(RuntimeError):
        workspace.close_document(document.document_id)
    workspace.close_document(document.document_id, force=True)
    assert workspace.active_document is None


def test_close_active_document_selects_remaining(tmp_path):
    workspace = manager(tmp_path)
    first = workspace.open_document(title="A")
    second = workspace.open_document(title="B")
    workspace.close_document(second.document_id)
    assert workspace.active_document is first


def test_tool_and_selection_revision_only_on_change(tmp_path):
    workspace = manager(tmp_path)
    initial = workspace.state.revision
    workspace.set_active_tool("wall")
    workspace.set_active_tool("wall")
    workspace.set_selection(["a", "a", "b"])
    workspace.set_selection(["a", "b"])
    assert workspace.state.active_tool == "wall"
    assert workspace.state.selection_ids == ("a", "b")
    assert workspace.state.revision == initial + 2


def test_serializer_roundtrip():
    state = WorkspaceState(name="Architecture", active_tool="wall")
    state.documents["doc"] = DocumentSession(document_id="doc", title="Modelo")
    restored = WorkspaceSerializer().loads(WorkspaceSerializer().dumps(state))
    assert restored.snapshot() == state.snapshot()


def test_serializer_rejects_non_object_json():
    with pytest.raises(ValueError):
        WorkspaceSerializer().loads("[]")


def test_layout_manager_save_load_list_delete(tmp_path):
    layouts = LayoutManager(tmp_path)
    state = WorkspaceState(active_tool="line")
    path = layouts.save("CAD", state)
    assert path.exists()
    assert layouts.list_layouts() == ("CAD",)
    assert layouts.load("CAD").active_tool == "line"
    assert layouts.delete("CAD")
    assert not layouts.delete("CAD")


def test_layout_name_validation(tmp_path):
    layouts = LayoutManager(tmp_path)
    with pytest.raises(ValueError):
        layouts.save("../bad", WorkspaceState())


def test_workspace_layout_restores_panels(tmp_path):
    workspace = manager(tmp_path)
    workspace.register_panel(PanelDescriptor("project", "Proyecto", DockArea.LEFT))
    workspace.docks.float("project", (1, 2, 300, 400))
    workspace.save_layout("Architecture")
    workspace.docks.dock("project", DockArea.RIGHT)
    workspace.load_layout("Architecture")
    state = workspace.panels.require("project")
    assert state.floating
    assert state.geometry == (1, 2, 300, 400)


def test_events_are_published(tmp_path):
    received = []
    workspace = manager(tmp_path, events=received.append)
    workspace.open_document(title="Modelo")
    assert received[-1].name == "workspace.document.opened"
    assert received[-1].payload["revision"] == 1


def test_graph_revision_integration_is_optional(tmp_path):
    class Graph:
        def __init__(self):
            self.values = {}
        def set_value(self, key, value):
            self.values[key] = value

    graph = Graph()
    workspace = manager(tmp_path, graph=graph)
    workspace.set_active_tool("rectangle")
    assert graph.values["workspace.revision"] == workspace.state.revision
