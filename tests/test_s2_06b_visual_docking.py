import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from gui.workspace import (
    DockArea,
    PanelDescriptor,
    QtUnavailableError,
    WindowLayoutSnapshot,
)

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from gui.workspace import (
    QtDockingController,
    WorkspaceManager,
    dock_area_to_qt,
    qt_area_to_dock_area,
)


@pytest.fixture(scope="session")
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def setup_workspace(tmp_path, app):
    window = QMainWindow()
    window.resize(900, 600)
    workspace = WorkspaceManager(tmp_path / "layouts")
    controller = QtDockingController(window, workspace)
    return window, workspace, controller


def descriptor(panel_id="properties", area=DockArea.RIGHT):
    return PanelDescriptor(panel_id, panel_id.title(), area)


def test_area_mapping_roundtrip():
    for area in (DockArea.LEFT, DockArea.RIGHT, DockArea.TOP, DockArea.BOTTOM):
        assert qt_area_to_dock_area(dock_area_to_qt(area)) is area


def test_register_panel_creates_dock(setup_workspace):
    window, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("Contenido"))
    assert dock.objectName() == "aias.dock.properties"
    assert controller.dock_widget("properties") is dock
    assert "properties" in workspace.registry


def test_register_panel_accepts_factory(setup_workspace):
    _, _, controller = setup_workspace
    dock = controller.register_panel(descriptor("project"), lambda: QLabel("Proyecto"))
    assert dock.widget().text() == "Proyecto"


def test_duplicate_visual_panel_rejected(setup_workspace):
    _, _, controller = setup_workspace
    controller.register_panel(descriptor(), QLabel("A"))
    with pytest.raises(KeyError):
        controller.register_panel(descriptor(), QLabel("B"))


def test_show_and_hide_panel(setup_workspace):
    _, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    controller.hide_panel("properties")
    assert not workspace.panels.require("properties").visible
    assert not dock.isVisible()
    controller.show_panel("properties")
    assert workspace.panels.require("properties").visible


def test_dock_left_updates_qt_and_state(setup_workspace):
    window, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    controller.dock_panel("properties", DockArea.LEFT)
    assert workspace.panels.require("properties").area is DockArea.LEFT
    assert qt_area_to_dock_area(window.dockWidgetArea(dock)) is DockArea.LEFT


def test_float_panel_updates_state(setup_workspace):
    _, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    controller.float_panel("properties", (15, 25, 320, 240))
    state = workspace.panels.require("properties")
    assert state.floating
    assert dock.isFloating()
    assert state.geometry == (15, 25, 320, 240)


def test_invalid_float_geometry_rejected(setup_workspace):
    _, _, controller = setup_workspace
    controller.register_panel(descriptor(), QLabel("A"))
    with pytest.raises(ValueError):
        controller.float_panel("properties", (0, 0, 0, 100))


def test_visibility_signal_updates_workspace(setup_workspace, app):
    _, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    dock.hide()
    app.processEvents()
    assert not workspace.panels.require("properties").visible


def test_location_signal_updates_workspace(setup_workspace, app):
    window, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    window.addDockWidget(dock_area_to_qt(DockArea.BOTTOM), dock)
    app.processEvents()
    assert workspace.panels.require("properties").area is DockArea.BOTTOM


def test_save_qt_layout_returns_text(setup_workspace):
    _, _, controller = setup_workspace
    controller.register_panel(descriptor(), QLabel("A"))
    state = controller.save_qt_layout()
    assert isinstance(state, str)
    assert state


def test_restore_empty_qt_layout_is_false(setup_workspace):
    _, _, controller = setup_workspace
    assert controller.restore_qt_layout("") is False


def test_restore_qt_layout(setup_workspace):
    _, _, controller = setup_workspace
    controller.register_panel(descriptor(), QLabel("A"))
    saved = controller.save_qt_layout()
    assert controller.restore_qt_layout(saved)


def test_sync_from_qt_captures_visibility(setup_workspace):
    _, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    dock.hide()
    controller.sync_from_qt()
    assert not workspace.state.panels["properties"].visible


def test_restore_all_applies_workspace_state(setup_workspace):
    _, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    state = workspace.panels.require("properties")
    state.visible = False
    controller.restore_all()
    assert not dock.isVisible()


def test_unregister_panel(setup_workspace):
    _, workspace, controller = setup_workspace
    controller.register_panel(descriptor(), QLabel("A"))
    controller.unregister_panel("properties")
    with pytest.raises(KeyError):
        controller.require_record("properties")
    with pytest.raises(KeyError):
        workspace.panels.require("properties")


def test_record_unknown_panel_rejected(setup_workspace):
    _, _, controller = setup_workspace
    with pytest.raises(KeyError):
        controller.require_record("missing")


def test_window_layout_snapshot_roundtrip():
    original = WindowLayoutSnapshot(
        workspace_name="Architecture",
        qt_state="abc",
        window_geometry=(1, 2, 800, 600),
        metadata={"screen": 1},
    )
    restored = WindowLayoutSnapshot.from_snapshot(original.snapshot())
    assert restored == original


def test_dock_factory_rejects_non_widget(setup_workspace):
    _, _, controller = setup_workspace
    with pytest.raises(TypeError):
        controller.register_panel(descriptor(), object())


def test_workspace_revision_changes_from_visual_signal(setup_workspace, app):
    _, workspace, controller = setup_workspace
    dock = controller.register_panel(descriptor(), QLabel("A"))
    before = workspace.state.revision
    dock.hide()
    app.processEvents()
    assert workspace.state.revision > before
