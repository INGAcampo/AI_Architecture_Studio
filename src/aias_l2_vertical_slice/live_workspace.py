"""Production live-workspace coordination for the validated Level 2 BIM vertical slice."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


class LiveWorkspaceIntegrationError(RuntimeError):
    """Raised when the live workspace cannot synchronize a requested BIM operation."""


@dataclass(frozen=True, slots=True)
class LiveWorkspaceSnapshot:
    """Describe the current synchronized production state exposed to Workspace 2."""

    revision: int
    selected_object_ids: tuple[str, ...]
    selected_node_id: str | None
    workspace_nodes: int
    dirty: bool
    persistence_path: str | None


class LiveWorkspaceSession:
    """Coordinate live BIM authoring, Workspace 2, properties, selection, history and persistence."""

    def __init__(
        self,
        bridge: Any,
        *,
        property_inspector: Any = None,
        workspace_widget: Any = None,
        visual_selection: Any = None,
        event_sink: Any = None,
    ) -> None:
        self.bridge = bridge
        self.property_inspector = property_inspector
        self.workspace_widget = workspace_widget
        self.visual_selection = visual_selection
        self.event_sink = event_sink
        self._saved_fingerprint: str | None = None
        self._persistence_path: Path | None = None
        self._started = False

    @property
    def service(self) -> Any:
        """Return the canonical vertical-slice service currently owned by the native bridge."""
        return self.bridge.service

    def start(self) -> LiveWorkspaceSnapshot:
        """Start live synchronization and publish the initial Workspace 2 projection."""
        self.bridge.synchronize()
        self._started = True
        self._saved_fingerprint = self._fingerprint()
        self._refresh_workspace_surface()
        self._synchronize_selection_surfaces()
        self._publish("l2.vertical_slice.live.started", revision=self.service.state.revision)
        return self.snapshot()

    def create_wall(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        **kwargs: Any,
    ) -> Any:
        """Create a wall through native history and immediately refresh all live surfaces."""
        self._require_started()
        wall = self.bridge.transact(lambda service: service.create_wall(start, end, **kwargs))
        self._after_model_change("wall.created", wall.id)
        return wall

    def create_door(
        self,
        wall_id: str,
        offset: float,
        width: float,
        height: float,
        sill_height: float = 0.0,
        **kwargs: Any,
    ) -> Any:
        """Create a hosted door and synchronize its Workspace 2 and relationship projections."""
        self._require_started()
        door = self.bridge.transact(
            lambda service: service.add_opening(
                "door",
                wall_id,
                offset,
                width,
                height,
                sill_height,
                **kwargs,
            )
        )
        self._after_model_change("door.created", door.id)
        return door

    def create_window(
        self,
        wall_id: str,
        offset: float,
        width: float,
        height: float,
        sill_height: float = 0.0,
        **kwargs: Any,
    ) -> Any:
        """Create a hosted window and synchronize its Workspace 2 and relationship projections."""
        self._require_started()
        window = self.bridge.transact(
            lambda service: service.add_opening(
                "window",
                wall_id,
                offset,
                width,
                height,
                sill_height,
                **kwargs,
            )
        )
        self._after_model_change("window.created", window.id)
        return window

    def create_room(
        self,
        wall_ids: list[str],
        name: str = "Room",
        **kwargs: Any,
    ) -> Any:
        """Create a bounded BIM room and refresh its live Workspace 2 representation."""
        self._require_started()
        room = self.bridge.transact(
            lambda service: service.create_room(wall_ids, name=name, **kwargs)
        )
        self._after_model_change("room.created", room.id)
        return room

    def set_property(self, object_id: str, key: str, value: Any) -> None:
        """Edit one BIM property under native history and propagate the resulting live state."""
        self._require_started()
        self.bridge.transact(
            lambda service: service.set_property(object_id, key, value)
        )
        self._after_model_change("property.changed", object_id, key=key, value=value)

    def select_from_workspace(self, object_id: str | None) -> LiveWorkspaceSnapshot:
        """Apply a Workspace 2 selection to the canonical model, viewport and Property Inspector."""
        return self._apply_selection(object_id, origin="workspace")

    def select_from_viewport(self, object_id: str | None) -> LiveWorkspaceSnapshot:
        """Apply a viewport selection to Workspace 2, canonical selection and Property Inspector."""
        return self._apply_selection(object_id, origin="viewport")

    def select_object(self, object_id: str | None) -> LiveWorkspaceSnapshot:
        """Select an object programmatically and synchronize all visible selection surfaces."""
        return self._apply_selection(object_id, origin="programmatic")

    def undo(self) -> bool:
        """Undo the last live model transaction and immediately refresh visible BIM state."""
        self._require_started()
        changed = bool(self.bridge.undo())
        if changed:
            self._refresh_workspace_surface()
            self._synchronize_selection_surfaces()
            self._publish("l2.vertical_slice.live.undo", revision=self.service.state.revision)
        return changed

    def redo(self) -> bool:
        """Redo the last live model transaction and immediately refresh visible BIM state."""
        self._require_started()
        changed = bool(self.bridge.redo())
        if changed:
            self._refresh_workspace_surface()
            self._synchronize_selection_surfaces()
            self._publish("l2.vertical_slice.live.redo", revision=self.service.state.revision)
        return changed

    def save(self, path: Path) -> Path:
        """Persist the live project through Omega and establish a clean production checkpoint."""
        self._require_started()
        saved = Path(self.bridge.save_native(Path(path)))
        self._persistence_path = saved
        self._saved_fingerprint = self._fingerprint()
        self._publish("l2.vertical_slice.live.saved", path=str(saved))
        return saved

    def reopen(self, path: Path | None = None) -> LiveWorkspaceSnapshot:
        """Reopen an Omega project and restore Workspace 2, properties and visible selection."""
        self._require_started()
        target = Path(path) if path is not None else self._persistence_path
        if target is None:
            raise LiveWorkspaceIntegrationError("persistence_path_required")
        self.bridge.load_native(target)
        self._persistence_path = target
        self._saved_fingerprint = self._fingerprint()
        self._refresh_workspace_surface()
        self._synchronize_selection_surfaces()
        self._publish("l2.vertical_slice.live.reopened", path=str(target))
        return self.snapshot()

    def bind_property_inspector(self, inspector: Any) -> None:
        """Replace the Property Inspector endpoint and synchronize the current selection into it."""
        self.property_inspector = inspector
        self._synchronize_property_inspector()

    def bind_workspace_widget(self, widget: Any) -> None:
        """Bind an existing Workspace 2 widget without replacing the application's Qt implementation."""
        self.workspace_widget = widget
        self._refresh_workspace_surface()
        self._synchronize_workspace_selection()

    def bind_visual_selection(self, target: Any) -> None:
        """Bind a viewport or renderer selection endpoint and push the current canonical selection."""
        self.visual_selection = target
        self._synchronize_visual_selection()

    def refresh(self) -> LiveWorkspaceSnapshot:
        """Force a canonical-to-native refresh while preserving live UI bindings."""
        self._require_started()
        self.bridge.synchronize()
        self._refresh_workspace_surface()
        self._synchronize_selection_surfaces()
        self._publish("l2.vertical_slice.live.refreshed", revision=self.service.state.revision)
        return self.snapshot()

    def snapshot(self) -> LiveWorkspaceSnapshot:
        """Return the current production synchronization state for tests, telemetry and handoff."""
        controller = getattr(self.bridge, "workspace_controller", None)
        if controller is None:
            workspace_nodes = 0
            selected_node_id = None
        else:
            tree = controller.tree.snapshot()
            workspace_nodes = len(tree.get("nodes", {}))
            selected_node_id = controller.state.selected_node_id
        return LiveWorkspaceSnapshot(
            revision=int(self.service.state.revision),
            selected_object_ids=tuple(str(x) for x in self.service.state.selection),
            selected_node_id=selected_node_id,
            workspace_nodes=workspace_nodes,
            dirty=self._saved_fingerprint is not None
            and self._saved_fingerprint != self._fingerprint(),
            persistence_path=str(self._persistence_path) if self._persistence_path else None,
        )

    def _after_model_change(self, event: str, object_id: str, **payload: Any) -> None:
        self._refresh_workspace_surface()
        self._synchronize_selection_surfaces()
        self._publish(
            f"l2.vertical_slice.live.{event}",
            object_id=object_id,
            revision=self.service.state.revision,
            **payload,
        )

    def _apply_selection(
        self,
        object_id: str | None,
        *,
        origin: str,
    ) -> LiveWorkspaceSnapshot:
        self._require_started()
        if object_id is None:
            self.service.state.selection = []
        else:
            self._require_object(object_id)
            self.service.select(object_id)
        self.bridge.synchronize()
        self._refresh_workspace_surface()
        self._synchronize_selection_surfaces()
        self._publish(
            "l2.vertical_slice.live.selection.changed",
            object_id=object_id,
            origin=origin,
        )
        return self.snapshot()

    def _refresh_workspace_surface(self) -> None:
        controller = getattr(self.bridge, "workspace_controller", None)
        if controller is None:
            controller = self.bridge.build_workspace_controller()
            self.bridge.workspace_controller = controller
        widget = self.workspace_widget
        if widget is None:
            return
        try:
            widget.controller = controller
        except Exception:
            pass
        rebuild = getattr(widget, "rebuild", None)
        if callable(rebuild):
            rebuild()

    def _synchronize_selection_surfaces(self) -> None:
        self._synchronize_workspace_selection()
        self._synchronize_visual_selection()
        self._synchronize_property_inspector()

    def _synchronize_workspace_selection(self) -> None:
        controller = getattr(self.bridge, "workspace_controller", None)
        selected = tuple(self.service.state.selection)
        object_id = selected[0] if selected else None
        if controller is not None:
            if object_id is None:
                controller.select_node(None)
            else:
                controller.select_object(object_id)
        widget = self.workspace_widget
        if widget is not None and object_id is not None:
            selector = getattr(widget, "select_object", None)
            if callable(selector):
                selector(object_id)

    def _synchronize_visual_selection(self) -> None:
        target = self.visual_selection
        if target is None:
            return
        identifiers = tuple(str(x) for x in self.service.state.selection)
        setter = getattr(target, "set_selection", None)
        if callable(setter):
            setter(identifiers)
            return
        if callable(target):
            target(identifiers)

    def _synchronize_property_inspector(self) -> None:
        inspector = self.property_inspector
        if inspector is None:
            return
        identifiers = tuple(self.service.state.selection)
        if not identifiers:
            clear = getattr(inspector, "clear", None)
            if callable(clear):
                clear()
            else:
                setter = getattr(inspector, "set_selection", None)
                if callable(setter):
                    setter(())
            return

        object_id = identifiers[0]
        obj = self._require_object(object_id)
        payload = {
            "object_id": object_id,
            "object_type": type(obj).__name__,
            "properties": dict(getattr(obj, "properties", {})),
            "object": obj,
        }

        for method_name in ("set_object", "inspect_object", "show_object"):
            method = getattr(inspector, method_name, None)
            if callable(method):
                try:
                    method(obj)
                except TypeError:
                    method(payload)
                return

        setter = getattr(inspector, "set_selection", None)
        if callable(setter):
            setter((object_id,))
            return

        if callable(inspector):
            inspector(payload)

    def _require_object(self, object_id: str) -> Any:
        state = self.service.state
        obj = (
            state.walls.get(object_id)
            or state.openings.get(object_id)
            or state.rooms.get(object_id)
        )
        if obj is None:
            raise LiveWorkspaceIntegrationError(f"unknown_object:{object_id}")
        return obj

    def _fingerprint(self) -> str:
        payload = json.dumps(
            self.service.state.to_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def _publish(self, name: str, **payload: Any) -> None:
        target = self.event_sink
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})

    def _require_started(self) -> None:
        if not self._started:
            raise LiveWorkspaceIntegrationError("live_workspace_not_started")
