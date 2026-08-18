"""Deterministic full-text and metadata search over engineering knowledge."""
from __future__ import annotations
from .models import KnowledgeUnit

class EngineeringSearchEngine:
    """Rank knowledge units by query relevance, domain and applicability filters."""
    def search(self, units: list[KnowledgeUnit], query: str, *, discipline: str | None = None) -> tuple[KnowledgeUnit, ...]:
        """Rank matching knowledge by text relevance and optional discipline."""
        q = query.lower().strip()
        scored = []
        for unit in units:
            if discipline and unit.discipline.lower() != discipline.lower():
                continue
            haystack = " ".join([
                unit.title, unit.discipline, unit.category, unit.source,
                " ".join(unit.keywords), str(unit.content), str(unit.requirements)
            ]).lower()
            score = haystack.count(q) if q else 1
            if score:
                scored.append((score, unit))
        scored.sort(key=lambda item: (-item[0], item[1].eku_id))
        return tuple(unit for _, unit in scored)
