from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReviewResult:
    sessions: int
    valid_records: int
    complete: bool
    issues: tuple[str, ...]


class EvidenceReview:
    minimum_sessions = 5

    def __init__(self, records_path: str | Path):
        self.path = Path(records_path)

    def run(self) -> ReviewResult:
        if not self.path.exists():
            return ReviewResult(0, 0, False, ("records file absent",))
        valid = 0
        issues: list[str] = []
        lines = [line for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for index, line in enumerate(lines, 1):
            try:
                payload = json.loads(line)
                digest = payload.pop("record_sha256")
                expected = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
                if digest != expected:
                    issues.append(f"record {index}: sha256 mismatch")
                elif not payload.get("consent_reference"):
                    issues.append(f"record {index}: consent missing")
                else:
                    valid += 1
            except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
                issues.append(f"record {index}: invalid format ({exc.__class__.__name__})")
        if valid < self.minimum_sessions:
            issues.append(f"minimum sessions not met: {valid}/{self.minimum_sessions}")
        return ReviewResult(len(lines), valid, valid >= self.minimum_sessions and not issues, tuple(issues))
