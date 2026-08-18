from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json

@dataclass(frozen=True)
class MonitorSnapshot:
    checked_at: str
    candidate_status: str
    changed: bool
    action: str

class CandidateMonitor:
    def __init__(self, status_path: str | Path): self.path = Path(status_path)
    def check(self, previous: str | None = None) -> MonitorSnapshot:
        status = "UNKNOWN"
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8")); status = str(data.get("status", data.get("candidate_status", "UNKNOWN")))
        changed = previous is not None and status != previous
        return MonitorSnapshot(datetime.now(timezone.utc).isoformat(), status, changed, "REVIEW_CHANGE" if changed else "NO_MUTATION")
