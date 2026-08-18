from __future__ import annotations

import json
from pathlib import Path

from .model import WorkspaceState


class WorkspaceSerializer:
    def dumps(self, state: WorkspaceState) -> str:
        return json.dumps(state.snapshot(), ensure_ascii=False, indent=2, sort_keys=True)

    def loads(self, text: str) -> WorkspaceState:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("El layout debe ser un objeto JSON")
        return WorkspaceState.from_snapshot(data)

    def save(self, state: WorkspaceState, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(self.dumps(state), encoding="utf-8")
        temporary.replace(target)
        return target

    def load(self, path: str | Path) -> WorkspaceState:
        return self.loads(Path(path).read_text(encoding="utf-8"))


class LayoutManager:
    def __init__(self, directory: str | Path, serializer: WorkspaceSerializer | None = None) -> None:
        self.directory = Path(directory)
        self.serializer = serializer or WorkspaceSerializer()

    def _path(self, name: str) -> Path:
        safe = name.strip()
        if not safe or any(char in safe for char in '\\/:*?"<>|'):
            raise ValueError("Nombre de layout no válido")
        return self.directory / f"{safe}.workspace.json"

    def save(self, name: str, state: WorkspaceState) -> Path:
        state.name = name
        return self.serializer.save(state, self._path(name))

    def load(self, name: str) -> WorkspaceState:
        return self.serializer.load(self._path(name))

    def delete(self, name: str) -> bool:
        path = self._path(name)
        if not path.exists():
            return False
        path.unlink()
        return True

    def list_layouts(self) -> tuple[str, ...]:
        if not self.directory.exists():
            return ()
        suffix = ".workspace.json"
        return tuple(
            path.name[:-len(suffix)]
            for path in sorted(self.directory.glob(f"*{suffix}"))
        )
