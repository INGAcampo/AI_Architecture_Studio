"""001F service: canonical project authoring with exact native Level/Grid activation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .native_project_integration import NativeProjectIntegrationService
from .native_level_grid import NativeLevelGridBridge


class ExactNativeProjectAuthoringService(NativeProjectIntegrationService):
    """Activate exact native Level/Grid authorities while preserving 001C behavior."""

    def __init__(self, project_name: str, *, discovery_path: Path, **kwargs: Any) -> None:
        super().__init__(project_name, discovery_path=discovery_path, **kwargs)
        self.level_grid = NativeLevelGridBridge()

    def add_level(self, name: str, elevation: float, **properties: Any) -> Any:
        """Commit canonical Level only if the exact native mirror also succeeds."""
        before = self.state.clone()
        history_len = len(self._history)
        redo = list(self._redo)
        try:
            canonical = super().add_level(name, elevation, **properties)
            self.level_grid.mirror_level(canonical)
            return canonical
        except Exception:
            self.state = before
            del self._history[history_len:]
            self._redo = redo
            raise

    def add_grid(
        self,
        name: str,
        start: tuple[float, float],
        end: tuple[float, float],
        **properties: Any,
    ) -> Any:
        """Commit canonical Grid only if the exact native mirror also succeeds."""
        before = self.state.clone()
        history_len = len(self._history)
        redo = list(self._redo)
        try:
            canonical = super().add_grid(name, start, end, **properties)
            self.level_grid.mirror_grid(canonical)
            return canonical
        except Exception:
            self.state = before
            del self._history[history_len:]
            self._redo = redo
            raise

    def exact_native_report(self) -> dict[str, Any]:
        """Combine 001C discovery status with active exact Level/Grid mirrors."""
        report = self.native_binding_report()
        report["exact_level_grid"] = self.level_grid.report()
        report["exact_native_domains"] = ["levels", "grids"]
        return report
