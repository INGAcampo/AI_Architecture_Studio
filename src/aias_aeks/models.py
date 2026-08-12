"""Canonical versioned engineering knowledge-unit contract."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class KnowledgeUnit:
    """Identified knowledge with domain, source, applicability and traceability metadata."""
    eku_id: str
    title: str
    discipline: str
    category: str
    source: str
    version: str
    status: str
    jurisdiction: str
    language: str
    keywords: list[str]
    relationships: list[dict[str, str]]
    requirements: list[dict[str, Any]]
    calculations: list[dict[str, Any]]
    deliverables: list[str]
    traceability: dict[str, Any]
    validation_rules: list[str]
    human_review_required: bool
    content: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize all knowledge content, provenance and relationship metadata."""
        return asdict(self)
