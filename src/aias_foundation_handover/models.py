"""Immutable evidence models used by the lifecycle handover framework."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class CustodyEvent:
    """Hash-linked record of a package-custody action."""
    event_id: str
    timestamp_utc: str
    action: str
    package_id: str
    actor: str
    previous_hash: str
    event_hash: str
    def to_dict(self) -> dict[str, Any]:
        """Serialize the custody event without losing actor, time or evidence references."""
        return asdict(self)

@dataclass(frozen=True, slots=True)
class KpiEvidence:
    """Classified acceleration, automation and reuse evidence."""
    classification: str
    baseline_hours: float
    actual_hours: float
    automated_hours: float
    reused_assets: int
    total_assets: int
    time_reduction: float
    automation_ratio: float
    reuse_ratio: float
    meets_45_percent_target: bool
    warning: str
    def to_dict(self) -> dict[str, Any]:
        """Serialize classified productivity evidence and derived ratios."""
        return asdict(self)
