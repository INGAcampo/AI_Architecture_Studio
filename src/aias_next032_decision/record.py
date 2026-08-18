from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApprovalDecisionRecord:
    decision_id: str
    decision: str
    authority_id: str
    scope: str
    decided_at: str
    evidence_sha256: str


class DecisionRecordBuilder:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def build(self, output: str | Path | None = None) -> ApprovalDecisionRecord:
        record = ApprovalDecisionRecord("AIAS-NEXT-032", "PENDING", "UNVERIFIED", "UNDEFINED", "", "")
        target = Path(output) if output else self.root / "engineering/aias/next032_decision/APPROVAL_DECISION.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(record), ensure_ascii=False, indent=2), encoding="utf-8")
        return record
