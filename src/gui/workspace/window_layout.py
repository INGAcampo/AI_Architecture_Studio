from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .manager import WorkspaceManager
from .qt_docking import QtDockingController


@dataclass(slots=True)
class WindowLayoutSnapshot:
    workspace_name: str
    qt_state: str
    window_geometry: tuple[int, int, int, int] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> dict[str, Any]:
        return {
            "workspace_name": self.workspace_name,
            "qt_state": self.qt_state,
            "window_geometry": list(self.window_geometry)
            if self.window_geometry else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_snapshot(cls, data: dict[str, Any]) -> "WindowLayoutSnapshot":
        geometry = data.get("window_geometry")
        return cls(
            workspace_name=str(data["workspace_name"]),
            qt_state=str(data.get("qt_state", "")),
            window_geometry=tuple(geometry) if geometry else None,
            metadata=dict(data.get("metadata", {})),
        )


class WindowLayoutCoordinator:
    def __init__(
        self,
        workspace: WorkspaceManager,
        docking: QtDockingController,
    ) -> None:
        self.workspace = workspace
        self.docking = docking

    def capture(self, name: str) -> WindowLayoutSnapshot:
        window = self.docking.main_window
        geometry = window.geometry()
        self.workspace.capture_panel_state()
        return WindowLayoutSnapshot(
            workspace_name=name,
            qt_state=self.docking.save_qt_layout(),
            window_geometry=(
                geometry.x(),
                geometry.y(),
                geometry.width(),
                geometry.height(),
            ),
        )

    def restore(self, snapshot: WindowLayoutSnapshot) -> bool:
        window = self.docking.main_window
        if snapshot.window_geometry:
            window.setGeometry(*snapshot.window_geometry)
        restored = self.docking.restore_qt_layout(snapshot.qt_state)
        self.docking.restore_all()
        return restored
