from __future__ import annotations

from collections.abc import Iterable

from aias_i18n import tr

from .model import DockArea, PanelDescriptor, PanelState


class PanelRegistry:
    def __init__(self) -> None:
        self._descriptors: dict[str, PanelDescriptor] = {}

    def register(self, descriptor: PanelDescriptor, *, replace: bool = False) -> None:
        if descriptor.panel_id in self._descriptors and not replace:
            raise KeyError(tr("workspace.error_panel_registered", panel_id=descriptor.panel_id))
        self._descriptors[descriptor.panel_id] = descriptor

    def unregister(self, panel_id: str) -> PanelDescriptor:
        try:
            return self._descriptors.pop(panel_id)
        except KeyError as exc:
            raise KeyError(tr("workspace.error_panel_unknown", panel_id=panel_id)) from exc

    def get(self, panel_id: str) -> PanelDescriptor:
        try:
            return self._descriptors[panel_id]
        except KeyError as exc:
            raise KeyError(tr("workspace.error_panel_unknown", panel_id=panel_id)) from exc

    def all(self) -> tuple[PanelDescriptor, ...]:
        return tuple(self._descriptors[key] for key in sorted(self._descriptors))

    def __contains__(self, panel_id: str) -> bool:
        return panel_id in self._descriptors


class PanelManager:
    def __init__(self, registry: PanelRegistry | None = None) -> None:
        self.registry = registry or PanelRegistry()
        self._states: dict[str, PanelState] = {}

    def activate(self, panel_id: str) -> PanelState:
        descriptor = self.registry.get(panel_id)
        state = self._states.get(panel_id)
        if state is None:
            state = PanelState(panel_id=panel_id, area=descriptor.default_area)
            self._states[panel_id] = state
        state.visible = True
        return state

    def hide(self, panel_id: str) -> PanelState:
        state = self.require(panel_id)
        state.visible = False
        return state

    def show(self, panel_id: str) -> PanelState:
        state = self.activate(panel_id)
        state.visible = True
        return state

    def remove(self, panel_id: str) -> PanelState:
        try:
            return self._states.pop(panel_id)
        except KeyError as exc:
            raise KeyError(tr("workspace.error_panel_inactive", panel_id=panel_id)) from exc

    def require(self, panel_id: str) -> PanelState:
        try:
            return self._states[panel_id]
        except KeyError as exc:
            raise KeyError(tr("workspace.error_panel_inactive", panel_id=panel_id)) from exc

    def states(self) -> tuple[PanelState, ...]:
        return tuple(self._states[key] for key in sorted(self._states))

    def restore(self, states: Iterable[PanelState]) -> None:
        restored = {}
        for state in states:
            if state.panel_id not in self.registry:
                continue
            restored[state.panel_id] = state
        self._states = restored


class DockManager:
    def __init__(self, panel_manager: PanelManager) -> None:
        self.panels = panel_manager

    def dock(self, panel_id: str, area: DockArea, *, order: int = 0) -> PanelState:
        if area is DockArea.FLOATING:
            return self.float(panel_id)
        state = self.panels.activate(panel_id)
        state.area = area
        state.floating = False
        state.order = int(order)
        return state

    def float(
        self,
        panel_id: str,
        geometry: tuple[int, int, int, int] | None = None,
    ) -> PanelState:
        if geometry is not None and (len(geometry) != 4 or min(geometry[2:]) <= 0):
            raise ValueError(tr("workspace.error_geometry"))
        state = self.panels.activate(panel_id)
        state.area = DockArea.FLOATING
        state.floating = True
        state.geometry = geometry
        return state

    def set_auto_hide(self, panel_id: str, enabled: bool) -> PanelState:
        state = self.panels.activate(panel_id)
        state.auto_hide = bool(enabled)
        return state
