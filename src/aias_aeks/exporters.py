"""Portable JSON and catalog export for governed engineering knowledge."""
from __future__ import annotations
import json
from pathlib import Path
from .models import KnowledgeUnit

class KnowledgeExporter:
    """Serialize knowledge units and indexes without losing provenance metadata."""
    def to_json(self, unit: KnowledgeUnit, path: Path) -> Path:
        """Export a complete knowledge unit as readable JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(unit.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def to_markdown(self, unit: KnowledgeUnit, path: Path) -> Path:
        """Export a human-readable knowledge summary with provenance metadata."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# {unit.title}\n\n"
            f"- ID: `{unit.eku_id}`\n"
            f"- Discipline: `{unit.discipline}`\n"
            f"- Category: `{unit.category}`\n"
            f"- Version: `{unit.version}`\n"
            f"- Status: `{unit.status}`\n"
            f"- Source: `{unit.source}`\n",
            encoding="utf-8",
        )
        return path
