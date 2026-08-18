from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AuthorityResult:
    stage: str
    authority_id: str | None
    verified: bool
    approval_granted: bool
    reason: str


class AuthorityWorkflow:
    def __init__(self, evidence_path: str | Path):
        self.path = Path(evidence_path)

    def evaluate(self) -> AuthorityResult:
        if not self.path.exists():
            return AuthorityResult("INTAKE_PENDING", None, False, False, "evidence absent")
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        authority = payload.get("authority_id")
        verified = payload.get("authority_verified") is True
        approved = payload.get("approval_granted") is True
        if not authority:
            return AuthorityResult("REJECTED", None, False, False, "authority_id absent")
        if not verified:
            return AuthorityResult("AUTHORITY_VERIFICATION_PENDING", authority, False, False, "identity not independently verified")
        if not approved:
            return AuthorityResult("APPROVAL_PENDING", authority, True, False, "approval not explicitly granted")
        return AuthorityResult("APPROVED", authority, True, True, "explicit authority verification and approval")
