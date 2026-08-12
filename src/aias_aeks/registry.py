"""Unique standards and code-source registration for engineering knowledge."""
from __future__ import annotations
import json, hashlib
from pathlib import Path
from .models import KnowledgeUnit

class StandardsRegistry:
    """Register, retrieve and classify standards without silent identity replacement."""
    def __init__(self, path: Path) -> None:
        self.path = path
        self.records: dict[str, dict] = {}
        if path.exists():
            self.records = json.loads(path.read_text(encoding="utf-8"))

    def register(self, unit: KnowledgeUnit, file_path: Path) -> None:
        """Register a unique knowledge identity and its persisted path."""
        self.records[unit.eku_id] = {
            "title": unit.title,
            "discipline": unit.discipline,
            "category": unit.category,
            "version": unit.version,
            "status": unit.status,
            "source": unit.source,
            "sha256": hashlib.sha256(file_path.read_bytes()).hexdigest(),
        }

    def save(self) -> None:
        """Persist the deterministic standards registry as readable JSON."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.records, indent=2, ensure_ascii=False), encoding="utf-8")
