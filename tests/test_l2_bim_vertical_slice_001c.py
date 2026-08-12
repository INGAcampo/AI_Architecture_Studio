from pathlib import Path

from aias_l2_vertical_slice.native_integration import NativeVerticalSliceBridge
from aias_l2_vertical_slice.service import VerticalSliceService


def _project():
    """Build a deterministic canonical project for native integration tests."""
    service = VerticalSliceService()
    w1 = service.create_wall((0, 0), (6, 0), properties={"level": "L1"})
    w2 = service.create_wall((6, 0), (6, 4), properties={"level": "L1"})
    w3 = service.create_wall((6, 4), (0, 4), properties={"level": "L1"})
    w4 = service.create_wall((0, 4), (0, 0), properties={"level": "L1"})
    door = service.add_opening("door", w1.id, 1, 0.9, 2.1)
    window = service.add_opening("window", w2.id, 1, 1.2, 1.2, 0.9)
    room = service.create_room([w1.id, w2.id, w3.id, w4.id], name="Office")
    service.select(w1.id, door.id)
    return service, (w1, w2, w3, w4), door, window, room


def test_native_authoring_stack_hosts_openings_and_rooms():
    """Synchronize canonical objects into the native BIM authoring engines."""
    service, walls, door, window, room = _project()
    bridge = NativeVerticalSliceBridge(service)
    report = bridge.synchronize()
    assert report.walls == 4
    assert report.doors == 1
    assert report.windows == 1
    assert report.rooms == 1
    assert report.relationships == 6
    assert len(bridge.wall_engine.openings.for_wall(walls[0].id)) == 1
    assert len(bridge.wall_engine.openings.for_wall(walls[1].id)) == 1
    assert bridge.room_engine.quantities(bridge.native_rooms[room.id]).area == 24.0


def test_native_relationship_propagation_reaches_hosted_opening():
    """Use the native smart relationship graph to calculate propagation impact."""
    service, walls, door, _, _ = _project()
    bridge = NativeVerticalSliceBridge(service)
    bridge.synchronize()
    report = bridge.propagation_report(walls[0].id, "property_changed")
    assert report.success
    assert door.id in report.affected_objects
    assert (door.id, "refresh_properties") in report.ordered_actions


def test_native_history_owns_transaction_undo_and_redo():
    """Execute a canonical mutation under the native CAD history manager."""
    service, walls, door, _, _ = _project()
    bridge = NativeVerticalSliceBridge(service)
    bridge.synchronize()
    bridge.transact(lambda target: target.set_property(walls[0].id, "level", "L2"))
    assert service.state.walls[walls[0].id].properties["level"] == "L2"
    assert service.state.openings[door.id].properties["level"] == "L2"
    assert bridge.undo()
    assert service.state.walls[walls[0].id].properties["level"] == "L1"
    assert bridge.redo()
    assert service.state.walls[walls[0].id].properties["level"] == "L2"


def test_native_omega_persistence_round_trip(tmp_path: Path):
    """Round-trip the complete canonical state through the native Omega serializer."""
    service, _, _, _, _ = _project()
    bridge = NativeVerticalSliceBridge(service)
    bridge.synchronize()
    before = service.state.to_dict()
    path = bridge.save_native(tmp_path / "vertical_slice_native.json")
    restored = bridge.load_native(path)
    assert restored.state.to_dict() == before


def test_workspace2_and_native_selection_are_synchronized():
    """Project canonical objects and selection into native Workspace 2 services."""
    service, walls, door, _, _ = _project()
    bridge = NativeVerticalSliceBridge(service)
    report = bridge.synchronize()
    snapshot = bridge.workspace_snapshot()
    nodes = snapshot["tree"]["nodes"]
    assert report.selected_objects == 2
    assert len(bridge.selection.all()) == 2
    assert f"instance.{walls[0].id}" in nodes
    assert f"instance.{door.id}" in nodes
    assert snapshot["state"]["selected_node_id"] == f"instance.{walls[0].id}"
