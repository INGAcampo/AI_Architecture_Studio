from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from aias_next016_decision import DecisionGate


@dataclass(frozen=True)
class ReviewPackage:
    decision: str
    sessions: int
    valid_records: int
    checklist: tuple[str, ...]
    review_ready: bool


class ReviewPackageBuilder:
    def __init__(self, project_root: str | Path):
        self.root = Path(project_root)

    def build(self, output: str | Path | None = None) -> ReviewPackage:
        report = self.root / "engineering/aias/next015_intake/INTAKE_REPORT.json"
        decision = DecisionGate(report).evaluate()
        checklist = ("hash integrity", "consent references", "minimum five sessions", "human review approval")
        package = ReviewPackage(decision.decision, decision.sessions, decision.valid_records, checklist, decision.decision == "READY_FOR_REVIEW")
        target = Path(output) if output else self.root / "engineering/aias/next017_review/REVIEW_PACKAGE.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(package), ensure_ascii=False, indent=2), encoding="utf-8")
        return package
