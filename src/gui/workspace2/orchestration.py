"""Unified, recoverable session authority for Workspace 2.0."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from gui.workspace.model import DockArea, PanelDescriptor, WorkspaceState
from .shell import Workspace2Shell


SESSION_SCHEMA = "AIAS-WORKSPACE-2-SESSION-1.0"


def _canonical(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


class SessionIntegrityError(ValueError):
    """Raised when a recovery file is malformed, incompatible or altered."""


class Workspace2SessionAuthority:
    """Single authority over shell state and the existing WorkspaceManager state."""

    def __init__(self, workspace_manager, shell: Workspace2Shell | None = None) -> None:
        required = ("state", "panels", "events")
        if any(not hasattr(workspace_manager, name) for name in required):
            raise TypeError("workspace_manager_contract_not_satisfied")
        self.workspace = workspace_manager
        self.shell = shell or Workspace2Shell()

    def snapshot(self) -> dict[str, Any]:
        self.workspace.capture_panel_state()
        payload = {
            "schema": SESSION_SCHEMA,
            "shell": self.shell.snapshot(),
            "panel_descriptors": [
                {
                    "panel_id": item.panel_id,
                    "title": item.title,
                    "default_area": item.default_area.value,
                    "singleton": item.singleton,
                    "category": item.category,
                    "metadata": item.metadata,
                }
                for item in self.workspace.registry.all()
            ],
            "workspace": self.workspace.state.snapshot(),
        }
        return {"payload": payload, "sha256": hashlib.sha256(_canonical(payload)).hexdigest()}

    def save_recovery(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(json.dumps(self.snapshot(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(target)
        self.workspace.events.publish("workspace2.session.saved", path=str(target))
        return target

    def restore_recovery(self, path: str | Path) -> dict[str, Any]:
        try:
            envelope = json.loads(Path(path).read_text(encoding="utf-8"))
            payload = envelope["payload"]
            checksum = envelope["sha256"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise SessionIntegrityError("invalid_session_envelope") from exc
        actual = hashlib.sha256(_canonical(payload)).hexdigest()
        if actual != checksum:
            raise SessionIntegrityError("session_checksum_mismatch")
        if payload.get("schema") != SESSION_SCHEMA:
            raise SessionIntegrityError("unsupported_session_schema")
        shell_data = payload.get("shell", {})
        descriptor_data = payload.get("panel_descriptors", [])
        workspace_data = payload.get("workspace", {})
        try:
            restored_shell = Workspace2Shell(
                theme=str(shell_data["theme"]),
                jurisdiction=str(shell_data["jurisdiction"]),
                review_status=str(shell_data["review_status"]),
            )
            restored_shell.switch_profile(str(shell_data["profile"]))
            restored_state = WorkspaceState.from_snapshot(workspace_data)
            restored_descriptors = tuple(
                PanelDescriptor(
                    panel_id=str(item["panel_id"]),
                    title=str(item["title"]),
                    default_area=DockArea(item["default_area"]),
                    singleton=bool(item.get("singleton", True)),
                    category=str(item.get("category", "general")),
                    metadata=dict(item.get("metadata", {})),
                )
                for item in descriptor_data
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SessionIntegrityError("invalid_session_state") from exc
        # Commit only after the entire envelope has passed validation.
        self.shell = restored_shell
        self.workspace.state = restored_state
        for descriptor in restored_descriptors:
            if descriptor.panel_id not in self.workspace.registry:
                self.workspace.registry.register(descriptor)
        self.workspace.panels.restore(restored_state.panels.values())
        self.workspace.events.publish("workspace2.session.restored", path=str(path))
        return self.snapshot()

    def switch_profile(self, profile: str) -> None:
        self.shell.switch_profile(profile)
        self.workspace.state.name = profile
        self.workspace._changed("workspace2.profile.changed", profile=profile)

    def open_document(self, *args, **kwargs):
        return self.workspace.open_document(*args, **kwargs)

    def close_document(self, *args, **kwargs):
        return self.workspace.close_document(*args, **kwargs)

    @property
    def active_document(self):
        return self.workspace.active_document
