from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PublicationDecision:
    allowed: bool
    classification: str
    label: str
    reason: str


class MetricsPublicationGate:
    def __init__(self, snapshot: str | Path):
        self.path = Path(snapshot)

    def evaluate(self) -> PublicationDecision:
        if not self.path.exists():
            return PublicationDecision(False, "UNKNOWN", "NOT_PUBLISHABLE", "snapshot absent")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        acceleration = data.get("acceleration", {})
        audited = bool(acceleration.get("audited", False))
        classification = acceleration.get("classification", "UNKNOWN")
        if audited:
            return PublicationDecision(True, classification, "AUDITED_METRIC", "external or independent audit recorded")
        return PublicationDecision(True, classification, "REFERENCE_ESTIMATE_NOT_AUDITED", "publication permitted only with non-audited label")
