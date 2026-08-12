"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

class CompilationCache:
    """Execute the public CompilationCache operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def key_for(self, specification: dict) -> str:
        """Execute the public CompilationCache.key_for operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        payload = json.dumps(specification, sort_keys=True).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def has(self, key: str) -> bool:
        """Execute the public CompilationCache.has operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        return (self.root / f"{key}.json").exists()

    def put(self, key: str, payload: dict) -> Path:
        """Execute the public CompilationCache.put operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        path = self.root / f"{key}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def get(self, key: str) -> dict:
        """Return get from autonomous engineering planning and controlled execution using deterministic lookup rules."""
        return json.loads((self.root / f"{key}.json").read_text(encoding="utf-8"))
