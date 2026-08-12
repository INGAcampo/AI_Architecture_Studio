from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MonitorResult:
    status: str
    handoff_present: bool
    approval_evidence_present: bool
    reason: str


class ReviewMonitor:
    def __init__(self, handoff_path: str | Path):
        self.path = Path(handoff_path)

    def check(self) -> MonitorResult:
        if not self.path.exists():
            return MonitorResult("PENDING_HUMAN_REVIEW", False, False, "handoff manifest absent")
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        evidence = payload.get("approval_status") == "APPROVED_BY_INDEPENDENT_REVIEWER" and bool(payload.get("reviewer_reference"))
        return MonitorResult("APPROVED" if evidence else "PENDING_HUMAN_REVIEW", True, evidence, "explicit reviewer evidence" if evidence else "no explicit independent approval")
