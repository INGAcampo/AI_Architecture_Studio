"""Persistent repository for versioned engineering knowledge units."""
from __future__ import annotations
import json
from pathlib import Path
from .models import KnowledgeUnit

class KnowledgeRepository:
    """Store, retrieve and enumerate knowledge while preserving stable identities."""
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, eku_id: str) -> Path:
        return self.root / f"{eku_id}.json"

    def save(self, unit: KnowledgeUnit) -> Path:
        """Persist a knowledge unit under its stable identifier."""
        path = self._path(unit.eku_id)
        path.write_text(json.dumps(unit.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def get(self, eku_id: str) -> KnowledgeUnit:
        """Load a typed knowledge unit by stable identity."""
        data = json.loads(self._path(eku_id).read_text(encoding="utf-8"))
        return KnowledgeUnit(**data)

    def list_ids(self) -> tuple[str, ...]:
        """Return all persisted knowledge identities in sorted order."""
        return tuple(sorted(p.stem for p in self.root.glob("EKU-*.json")))

    def delete(self, eku_id: str) -> None:
        """Remove the exact persisted knowledge unit identified by the caller."""
        self._path(eku_id).unlink(missing_ok=True)
