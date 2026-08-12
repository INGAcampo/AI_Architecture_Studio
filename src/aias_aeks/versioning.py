"""Semantic version progression and immutable knowledge revision history."""
from __future__ import annotations
from dataclasses import dataclass, field
from .models import KnowledgeUnit

@dataclass(slots=True)
class KnowledgeVersionManager:
    """Validate version changes and retain earlier knowledge-unit snapshots."""
    history: dict[str, list[dict]] = field(default_factory=dict)

    def record(self, unit: KnowledgeUnit, note: str) -> None:
        """Append a deep snapshot of a knowledge version with a revision note."""
        self.history.setdefault(unit.eku_id, []).append({
            "version": unit.version,
            "status": unit.status,
            "note": note,
        })

    def versions(self, eku_id: str) -> tuple[str, ...]:
        """Return recorded semantic versions for a knowledge identity."""
        return tuple(item["version"] for item in self.history.get(eku_id, []))
