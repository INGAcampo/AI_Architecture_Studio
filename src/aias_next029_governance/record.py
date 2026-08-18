from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class GovernanceRecord:
    record_id: str
    candidate_status: str
    external_gates: str
    production_approval: str
    decision_owner: str


class GovernanceBuilder:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def build(self, output: str | Path | None = None) -> GovernanceRecord:
        record = GovernanceRecord("AIAS-NEXT-029", "CANDIDATE", "PENDING", "NOT_GRANTED", "UNASSIGNED")
        target = Path(output) if output else self.root / "engineering/aias/next029_governance/GOVERNANCE_RECORD.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(record), ensure_ascii=False, indent=2), encoding="utf-8")
        return record
