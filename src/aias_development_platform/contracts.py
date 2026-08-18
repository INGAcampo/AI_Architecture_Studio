"""Stable cross-generation contracts for the AIAS Development Platform."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DevelopmentJob:
    """Request one governed and isolated specification-driven production run."""
    job_id: str
    specification: Path
    workspace: Path
    mode: str = "auto"
    correlation_id: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DevelopmentResult:
    """Normalize engine-specific output into one auditable result envelope."""
    job_id: str
    engine: str
    certified: bool
    artifacts: tuple[str, ...]
    evidence: dict
