"""JSON importer for typed engineering knowledge units."""
from __future__ import annotations
import json
from pathlib import Path
from .models import KnowledgeUnit
from .validation import KnowledgeValidator

class JSONKnowledgeImporter:
    """Decode external JSON and construct a validated knowledge-unit record."""
    def load(self, path: Path) -> KnowledgeUnit:
        """Load JSON and construct a typed knowledge unit."""
        unit = KnowledgeUnit(**json.loads(path.read_text(encoding="utf-8")))
        issues = KnowledgeValidator().validate(unit)
        if issues:
            raise ValueError(";".join(issues))
        return unit
