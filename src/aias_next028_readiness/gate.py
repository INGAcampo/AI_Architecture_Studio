from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReadinessDecision:
    decision: str
    reason: str
    external_gates_pending: bool


class ReleaseReadinessGate:
    def __init__(self, verification_path: str | Path, bundle_path: str | Path):
        self.verification = Path(verification_path)
        self.bundle = Path(bundle_path)

    def evaluate(self) -> ReadinessDecision:
        if not self.verification.exists() or not self.bundle.exists():
            return ReadinessDecision("HOLD_CANDIDATE", "verification or evidence bundle absent", True)
        bundle = json.loads(self.bundle.read_text(encoding="utf-8"))
        external_pending = bool(bundle.get("external_gates_pending", True))
        if external_pending:
            return ReadinessDecision("READY_FOR_EXTERNAL_APPROVAL", "local evidence assembled; external gates remain", True)
        return ReadinessDecision("READY_FOR_RELEASE_REVIEW", "local and external gates represented", False)
