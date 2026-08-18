from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from aias_next013_review import EvidenceReview


@dataclass(frozen=True)
class IntakeReport:
    source: str
    sessions: int
    valid_records: int
    complete: bool
    issues: tuple[str, ...]


class EvidenceIntakeReport:
    def __init__(self, project_root: str | Path):
        self.root = Path(project_root)

    def generate(self, output: str | Path | None = None) -> IntakeReport:
        source = self.root / "engineering/aias/usability_campaign/SESSION_RECORDS.jsonl"
        result = EvidenceReview(source).run()
        report = IntakeReport(str(source), result.sessions, result.valid_records, result.complete, result.issues)
        destination = Path(output) if output else self.root / "engineering/aias/next015_intake/INTAKE_REPORT.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")
        return report
