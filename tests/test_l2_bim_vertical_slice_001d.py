"""End-to-end production closure tests for the Level 2 BIM live Workspace integration."""
from pathlib import Path

from aias_l2_vertical_slice.live_workspace import LiveWorkspaceSession
from aias_l2_vertical_slice.native_integration import NativeVerticalSliceBridge
from aias_l2_vertical_slice.service import VerticalSliceService


class _Inspector:
    def __init__(self):
        self.current = None
        self.clear_count = 0

    def set_object(self, obj):
        self.current = obj

    def clear(self):
        self.current = None
        self.clear_count += 1


class _VisualSelection:
    def __init__(self):
        self.identifiers = ()

    def set_selection(self, identifiers):
        self.identifiers = tuple(identifiers)


class _WorkspaceWidget:
    def __init__(self):
        self.controller = None
        self.rebuild_count = 0
        self.selected = None

    def rebuild(self):
        self.rebuild_count += 1

    def select_object(self, object_id):
        self.selected = object_id
        return True


def _session():
    inspector = _Inspector()
    visual = _VisualSelection()
    widget = _WorkspaceWidget()
    bridge = NativeVerticalSliceBridge(VerticalSliceService())
    session = LiveWorkspaceSession(
        bridge,
        property_inspector=inspector,
        workspace_widget=widget,
        visual_selection=visual,
    )
    session.start()
    return session, inspector, visual, widget


def _rectangle(session):
    w1 = session.create_wall((0, 0), (6, 0), properties={"level": "L1"})
    w2 = session.create_wall((6, 0), (6, 4), properties={"level": "L1"})
    w3 = session.create_wall((6, 4), (0, 4), properties={"level": "L1"})
    w4 = session.create_wall((0, 4), (0, 0), properties={"level": "L1"})
    return w1, w2, w3, w4


def test_live_authoring_reaches_workspace2_and_native_engines():
    session, _, _, widget = _session()
    walls = _rectangle(session)
    door = session.create_door(walls[0].id, 1, 0.9, 2.1)
    window = session.create_window(walls[1].id, 1, 1.2, 1.2, 0.9)
    room = session.create_room([wall.id for wall in walls], name="Office")
    snap = session.snapshot()
    assert len(session.bridge.wall_engine.walls) == 4
    assert len(session.bridge.door_engine.doors) == 1
    assert len(session.bridge.window_engine.windows) == 1
    assert len(session.bridge.native_rooms) == 1
    assert snap.workspace_nodes >= 8
    assert f"instance.{door.id}" in session.bridge.workspace_controller.tree.snapshot()["nodes"]
    assert f"instance.{window.id}" in session.bridge.workspace_controller.tree.snapshot()["nodes"]
    assert f"instance.{room.id}" in session.bridge.workspace_controller.tree.snapshot()["nodes"]
    assert widget.rebuild_count > 0


def test_workspace_and_viewport_selection_are_bidirectional():
    session, inspector, visual, widget = _session()
    wall = session.create_wall((0, 0), (5, 0), properties={"level": "L1"})
    session.select_from_workspace(wall.id)
    assert session.service.state.selection == [wall.id]
    assert inspector.current.id == wall.id
    assert visual.identifiers == (wall.id,)
    assert widget.selected == wall.id
    assert session.snapshot().selected_node_id == f"instance.{wall.id}"

    session.select_from_viewport(None)
    assert session.service.state.selection == []
    assert inspector.current is None
    assert visual.identifiers == ()


def test_property_inspector_edit_propagates_and_is_visible_after_undo_redo():
    session, inspector, _, _ = _session()
    wall = session.create_wall((0, 0), (5, 0), properties={"level": "L1"})
    door = session.create_door(wall.id, 1, 0.9, 2.1)
    session.select_object(wall.id)
    session.set_property(wall.id, "level", "L2")
    assert session.service.state.walls[wall.id].properties["level"] == "L2"
    assert session.service.state.openings[door.id].properties["level"] == "L2"
    assert inspector.current.properties["level"] == "L2"

    assert session.undo()
    assert session.service.state.walls[wall.id].properties["level"] == "L1"
    assert session.redo()
    assert session.service.state.walls[wall.id].properties["level"] == "L2"


def test_omega_save_reopen_restores_geometry_properties_and_selection(tmp_path: Path):
    session, inspector, visual, _ = _session()
    walls = _rectangle(session)
    door = session.create_door(walls[0].id, 1, 0.9, 2.1)
    session.create_window(walls[1].id, 1, 1.2, 1.2, 0.9)
    session.create_room([wall.id for wall in walls], name="Office")
    session.set_property(walls[0].id, "discipline", "Architecture")
    session.select_object(door.id)
    before = session.service.state.to_dict()

    path = session.save(tmp_path / "live_workspace.aias.json")
    assert path.exists()
    assert session.snapshot().dirty is False

    session.set_property(walls[0].id, "discipline", "Changed")
    assert session.snapshot().dirty is True
    snap = session.reopen(path)
    assert session.service.state.to_dict() == before
    assert snap.dirty is False
    assert inspector.current.id == door.id
    assert visual.identifiers == (door.id,)


def test_live_events_and_refresh_are_deterministic():
    events = []
    bridge = NativeVerticalSliceBridge(VerticalSliceService())
    session = LiveWorkspaceSession(
        bridge,
        event_sink=lambda name, payload: events.append((name, payload)),
    )
    first = session.start()
    wall = session.create_wall((0, 0), (3, 0))
    second = session.refresh()
    assert first.workspace_nodes >= 5
    assert second.workspace_nodes > first.workspace_nodes
    assert any(name.endswith("wall.created") for name, _ in events)
    assert any(name.endswith("refreshed") for name, _ in events)
    assert wall.id in session.service.state.walls
