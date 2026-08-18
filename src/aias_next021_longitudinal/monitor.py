from __future__ import annotations

import json
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LongitudinalResult:
    records: int
    first_recorded_at: str | None
    last_recorded_at: str | None
    observation_days: float
    sufficient_for_365_days: bool


class LongitudinalMonitor:
    def __init__(self, records_path: str | Path):
        self.path = Path(records_path)

    def measure(self) -> LongitudinalResult:
        if not self.path.exists():
            return LongitudinalResult(0, None, None, 0.0, False)
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        dates = []
        for row in rows:
            stamp = row.get("recorded_at")
            if stamp:
                dates.append(datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(timezone.utc))
        if not dates:
            return LongitudinalResult(len(rows), None, None, 0.0, False)
        span = (max(dates) - min(dates)).total_seconds() / 86400
        return LongitudinalResult(len(rows), min(dates).isoformat(), max(dates).isoformat(), span, span >= 365)
