from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IntakeDecision:
    accepted: bool
    status: str
    reason: str


class ExternalApprovalIntake:
    required = ("authority_id", "document_reference", "document_sha256", "issued_at")

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def inspect(self) -> IntakeDecision:
        if not self.path.exists():
            return IntakeDecision(False, "PENDING_EXTERNAL_EVIDENCE", "evidence record absent")
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        missing = [key for key in self.required if not payload.get(key)]
        if missing:
            return IntakeDecision(False, "REJECTED_INCOMPLETE", "missing: " + ", ".join(missing))
        return IntakeDecision(True, "RECEIVED_FOR_AUTHORITY_REVIEW", "schema complete; authenticity still requires authority verification")
