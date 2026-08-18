"""Public module supporting the coordinated multi-studio desktop shell."""
import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass(slots=True)
class WorkspaceState:
    """Execute the public WorkspaceState operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    active_studio: str = "home"
    open_documents: list[dict] = None
    geometry: bytes = b""

    def __post_init__(self) -> None:
        if self.open_documents is None:
            self.open_documents = []

class WorkspaceStateStore:
    """Execute the public WorkspaceStateStore operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: WorkspaceState) -> None:
        """Persist save for the coordinated multi-studio desktop shell in its stable external representation."""
        data = asdict(state)
        data["geometry"] = state.geometry.hex()
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self) -> WorkspaceState:
        """Load load for the coordinated multi-studio desktop shell while preserving typed state."""
        if not self.path.exists():
            return WorkspaceState()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return WorkspaceState(
            active_studio=data.get("active_studio", "home"),
            open_documents=data.get("open_documents", []),
            geometry=bytes.fromhex(data.get("geometry", "")),
        )
