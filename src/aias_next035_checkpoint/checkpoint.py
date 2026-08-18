from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckpointResult:
    decision: str
    blockers: tuple[str, ...]
    traceable: bool


class GovernanceCheckpoint:
    def __init__(self, governance_path: str | Path, external_status_path: str | Path):
        self.governance = Path(governance_path)
        self.external = Path(external_status_path)

    def evaluate(self) -> CheckpointResult:
        blockers = []
        if not self.governance.exists():
            blockers.append("governance record absent")
        if not self.external.exists():
            blockers.append("external status absent")
        if not blockers:
            governance = json.loads(self.governance.read_text(encoding="utf-8"))
            external = json.loads(self.external.read_text(encoding="utf-8"))
            if governance.get("production_approval") != "GRANTED":
                blockers.append("production approval not granted")
            if not external.get("all_approved", False):
                blockers.append("external gates not all approved")
        return CheckpointResult("HOLD" if blockers else "PROCEED_TO_RELEASE_REVIEW", tuple(blockers), True)
