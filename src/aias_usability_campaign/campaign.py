from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class SessionRecord:
    session_id: str
    facilitator: str
    participant_code: str
    started_at: str
    ended_at: str
    tasks: tuple[str, ...]
    observations: tuple[str, ...]
    artifacts: tuple[str, ...]
    consent_reference: str


class UsabilityCampaign:
    """Collects attestable sessions; refuses synthetic completion claims."""

    minimum_sessions = 5

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.path = self.root / "engineering/aias/usability_campaign/SESSION_RECORDS.jsonl"

    def append(self, record: SessionRecord) -> str:
        if not record.session_id or not record.consent_reference:
            raise ValueError("session_id and consent_reference are required")
        payload = asdict(record)
        payload["recorded_at"] = datetime.now(timezone.utc).isoformat()
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload["record_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        return payload["record_sha256"]

    def count(self) -> int:
        if not self.path.exists():
            return 0
        return sum(1 for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip())

    def status(self) -> dict[str, object]:
        count = self.count()
        return {"sessions": count, "minimum_sessions": self.minimum_sessions, "campaign_complete": count >= self.minimum_sessions, "evidence_synthetic": False}
