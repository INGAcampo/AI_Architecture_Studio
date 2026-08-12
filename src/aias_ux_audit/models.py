"""Domain models for reproducible UX audits."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JourneyRequirement:
    requirement_id: str
    description: str
    evidence_any: tuple[str, ...]


@dataclass(frozen=True)
class Journey:
    journey_id: str
    name: str
    outcome: str
    target_minutes: int
    requirements: tuple[JourneyRequirement, ...]

