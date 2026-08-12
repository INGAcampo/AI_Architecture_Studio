from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DecisionResult:
    decision: str
    sessions: int
    valid_records: int
    reason: str


class DecisionGate:
    minimum_sessions = 5

    def __init__(self, report_path: str | Path):
        self.path = Path(report_path)

    def evaluate(self) -> DecisionResult:
        if not self.path.exists():
            return DecisionResult("CONTINUE_COLLECTION", 0, 0, "intake report absent")
        report = json.loads(self.path.read_text(encoding="utf-8"))
        sessions = int(report.get("sessions", 0))
        valid = int(report.get("valid_records", 0))
        complete = bool(report.get("complete", False))
        if complete and sessions >= self.minimum_sessions and valid >= self.minimum_sessions:
            return DecisionResult("READY_FOR_REVIEW", sessions, valid, "minimum evidence threshold met")
        return DecisionResult("CONTINUE_COLLECTION", sessions, valid, "minimum evidence threshold not met")
