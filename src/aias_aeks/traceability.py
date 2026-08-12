"""Traceability projection from knowledge sources to engineering consumers."""
from __future__ import annotations
from .models import KnowledgeUnit

class KnowledgeTraceabilityEngine:
    """Expose source, requirement and downstream-consumer relationships per unit."""
    def matrix(self, unit: KnowledgeUnit) -> dict:
        """Project knowledge provenance, requirements and consumer relationships."""
        return {
            "eku_id": unit.eku_id,
            "source": unit.source,
            "requirements": [r.get("id") for r in unit.requirements],
            "deliverables": list(unit.deliverables),
            "relationships": list(unit.relationships),
            "human_review_required": unit.human_review_required,
        }
