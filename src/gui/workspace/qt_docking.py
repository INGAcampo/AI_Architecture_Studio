from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from aias_i18n import tr

from .model import DockArea, PanelDescriptor, PanelState
from .manager import WorkspaceManager

try:
    from PySide6.QtCore import QByteArray, Qt
    from PySide6.QtWidgets import QDockWidget, QMainWindow, QWidget
except ImportError:  # Permite importar y probar el módulo sin Qt instalado.
    QByteArray = None
    Qt = None
    QDockWidget = None
    QMainWindow = None
    QWidget = None


class QtUnavailableError(RuntimeError):
    pass


def require_qt() -> None:
    if QDockWidget is None or QMainWindow is None or Qt is None:
        raise QtUnavailableError(
            tr("workspace.error_qt_unavailable")
        )


def dock_area_to_qt(area: DockArea):
    require_qt()
    mapping = {
        DockArea.LEFT: Qt.LeftDockWidgetArea,
        DockArea.RIGHT: Qt.RightDockWidgetArea,
        DockArea.TOP: Qt.TopDockWidgetArea,
        DockArea.BOTTOM: Qt.BottomDockWidgetArea,
        DockArea.CENTER: Qt.RightDockWidgetArea,
        DockArea.FLOATING: Qt.RightDockWidgetArea,
    }
    return mapping[area]


def qt_area_to_dock_area(qt_area) -> DockArea:
    require_qt()
    mapping = {
        Qt.LeftDockWidgetArea: DockArea.LEFT,
        Qt.RightDockWidgetArea: DockArea.RIGHT,
        Qt.TopDockWidgetArea: DockArea.TOP,
        Qt.BottomDockWidgetArea: DockArea.BOTTOM,
    }
    return mapping.get(qt_area, DockArea.RIGHT)


@dataclass(slots=True)
class DockWidgetRecord:
    panel_id: str
    dock_widget: Any
    content_widget: Any


class DockWidgetFactory:
    """Crea QDockWidget consistentes para todos los paneles de AIAS."""

    def create(
        self,
        descriptor: PanelDescriptor,
        content_widget: Any,
        parent: Any = None,
    ) -> Any:
        require_qt()
        if not isinstance(content_widget, QWidget):
            raise TypeError(tr("workspace.error_content_widget"))

        dock = QDockWidget(descriptor.title, parent)
        dock.setObjectName(f"aias.dock.{descriptor.panel_id}")
        dock.setWidget(content_widget)
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea
            | Qt.RightDockWidgetArea
            | Qt.TopDockWidgetArea
            | Qt.BottomDockWidgetArea
        )
        dock.setFeatures(
            QDockWidget.DockWidgetClosable
            | QDockWidget.DockWidgetMovable
            | QDockWidget.DockWidgetFloatable
        )
        return dock


class QtDockingController:
    """
    Adaptador visual entre WorkspaceManager y QMainWindow/QDockWidget.

    WorkspaceManager conserva el estado canónico. Este controlador traduce
    señales visuales de Qt a PanelState y aplica PanelState a la interfaz.
    """

    def __init__(
        self,
        main_window: Any,
        workspace: WorkspaceManager,
        *,
        factory: DockWidgetFactory | None = None,
    ) -> None:
        require_qt()
        if not isinstance(main_window, QMainWindow):
            raise TypeError(tr("workspace.error_main_window"))

        self.main_window = main_window
        self.workspace = workspace
        self.factory = factory or DockWidgetFactory()
        self._records: dict[str, DockWidgetRecord] = {}
        self._restoring = False

    def register_panel(
        self,
        descriptor: PanelDescriptor,
        widget_or_factory: Any | Callable[[], Any],
    ) -> Any:
        if descriptor.panel_id in self._records:
            raise KeyError(tr("workspace.error_visual_registered", panel_id=descriptor.panel_id))

        if descriptor.panel_id not in self.workspace.registry:
            self.workspace.register_panel(descriptor)

        content = widget_or_factory() if callable(widget_or_factory) else widget_or_factory
        dock = self.factory.create(descriptor, content, self.main_window)
        self._records[descriptor.panel_id] = DockWidgetRecord(
            panel_id=descriptor.panel_id,
            dock_widget=dock,
            content_widget=content,
        )

        state = self.workspace.panels.activate(descriptor.panel_id)
        self.main_window.addDockWidget(dock_area_to_qt(state.area), dock)
        self._connect_signals(descriptor.panel_id, dock)
        self.apply_panel_state(descriptor.panel_id)
        return dock

    def unregister_panel(self, panel_id: str) -> None:
        record = self.require_record(panel_id)
        self.main_window.removeDockWidget(record.dock_widget)
        record.dock_widget.deleteLater()
        self._records.pop(panel_id)
        try:
            self.workspace.panels.remove(panel_id)
        except KeyError:
            pass

    def require_record(self, panel_id: str) -> DockWidgetRecord:
        try:
            return self._records[panel_id]
        except KeyError as exc:
            raise KeyError(tr("workspace.error_visual_unknown", panel_id=panel_id)) from exc

    def dock_widget(self, panel_id: str) -> Any:
        return self.require_record(panel_id).dock_widget

    def show_panel(self, panel_id: str) -> None:
        state = self.workspace.panels.show(panel_id)
        self.apply_panel_state(panel_id, state)

    def hide_panel(self, panel_id: str) -> None:
        state = self.workspace.panels.hide(panel_id)
        self.apply_panel_state(panel_id, state)

    def dock_panel(self, panel_id: str, area: DockArea, order: int = 0) -> None:
        state = self.workspace.docks.dock(panel_id, area, order=order)
        self.apply_panel_state(panel_id, state)

    def float_panel(
        self,
        panel_id: str,
        geometry: tuple[int, int, int, int] | None = None,
    ) -> None:
        state = self.workspace.docks.float(panel_id, geometry)
        self.apply_panel_state(panel_id, state)

    def apply_panel_state(
        self,
        panel_id: str,
        state: PanelState | None = None,
    ) -> None:
        record = self.require_record(panel_id)
        state = state or self.workspace.panels.require(panel_id)
        dock = record.dock_widget

        self._restoring = True
        try:
            if state.floating or state.area is DockArea.FLOATING:
                dock.setFloating(True)
                if state.geometry:
                    dock.setGeometry(*state.geometry)
            else:
                dock.setFloating(False)
                self.main_window.addDockWidget(dock_area_to_qt(state.area), dock)

            dock.setVisible(state.visible)
        finally:
            self._restoring = False

    def restore_all(self) -> None:
        for panel_id in tuple(self._records):
            if panel_id in {state.panel_id for state in self.workspace.panels.states()}:
                self.apply_panel_state(panel_id)

    def save_qt_layout(self) -> str:
        raw = self.main_window.saveState()
        return bytes(raw.toBase64()).decode("ascii")

    def restore_qt_layout(self, encoded: str) -> bool:
        if not encoded:
            return False
        raw = QByteArray.fromBase64(encoded.encode("ascii"))
        self._restoring = True
        try:
            restored = bool(self.main_window.restoreState(raw))
        finally:
            self._restoring = False
        self.sync_from_qt()
        return restored

    def sync_from_qt(self) -> None:
        for panel_id, record in self._records.items():
            self._sync_record(panel_id, record.dock_widget)
        self.workspace.capture_panel_state()

    def _connect_signals(self, panel_id: str, dock: Any) -> None:
        dock.visibilityChanged.connect(
            lambda visible, pid=panel_id: self._on_visibility_changed(pid, visible)
        )
        dock.topLevelChanged.connect(
            lambda floating, pid=panel_id: self._on_floating_changed(pid, floating)
        )
        dock.dockLocationChanged.connect(
            lambda area, pid=panel_id: self._on_location_changed(pid, area)
        )

    def _on_visibility_changed(self, panel_id: str, visible: bool) -> None:
        if self._restoring:
            return
        state = self.workspace.panels.require(panel_id)
        if state.visible != bool(visible):
            state.visible = bool(visible)
            self.workspace._changed(
                "workspace.panel.visibility.changed",
                panel_id=panel_id,
                visible=state.visible,
            )

    def _on_floating_changed(self, panel_id: str, floating: bool) -> None:
        if self._restoring:
            return
        state = self.workspace.panels.require(panel_id)
        state.floating = bool(floating)
        if floating:
            state.area = DockArea.FLOATING
            dock = self.dock_widget(panel_id)
            geometry = dock.geometry()
            state.geometry = (
                geometry.x(),
                geometry.y(),
                geometry.width(),
                geometry.height(),
            )
        self.workspace._changed(
            "workspace.panel.floating.changed",
            panel_id=panel_id,
            floating=state.floating,
        )

    def _on_location_changed(self, panel_id: str, qt_area: Any) -> None:
        if self._restoring:
            return
        state = self.workspace.panels.require(panel_id)
        state.area = qt_area_to_dock_area(qt_area)
        state.floating = False
        self.workspace._changed(
            "workspace.panel.location.changed",
            panel_id=panel_id,
            area=state.area.value,
        )

    def _sync_record(self, panel_id: str, dock: Any) -> None:
        state = self.workspace.panels.require(panel_id)
        state.visible = dock.isVisible()
        state.floating = dock.isFloating()

        if state.floating:
            state.area = DockArea.FLOATING
            geometry = dock.geometry()
            state.geometry = (
                geometry.x(),
                geometry.y(),
                geometry.width(),
                geometry.height(),
            )
        else:
            state.area = qt_area_to_dock_area(
                self.main_window.dockWidgetArea(dock)
            )
