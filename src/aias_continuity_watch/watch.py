from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
@dataclass(frozen=True, slots=True)
class WatchDecision:
    current: str
    next_task: str
    action: str
    reason: str
@dataclass(slots=True)
class ContinuityWatch:
    def inspect(self, root: Path) -> WatchDecision:
        plan=json.loads((root/"engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json").read_text(encoding="utf-8"))
        next_task=str(plan.get("next", "")); current=str(plan.get("current", ""))
        if not next_task: return WatchDecision(current,"","STOP","No next task declared")
        if any(token in next_task.lower() for token in ("license","normative","professional","external","destructive")):
            return WatchDecision(current,next_task,"HOLD_FOR_AUTHORITY","Next task requires external or strategic authority")
        return WatchDecision(current,next_task,"CONTINUE_SAFE","Next task is declared and does not match protected stop rules")
