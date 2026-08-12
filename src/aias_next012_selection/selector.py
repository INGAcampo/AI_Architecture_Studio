from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SelectionResult:
    selected: str
    rationale: str
    deferred: tuple[str, ...]


class MacrodeliverySelector:
    """Selects only the declared next item; never invents external evidence."""

    def __init__(self, project_root: str | Path):
        self.root = Path(project_root)

    def select(self) -> SelectionResult:
        plan = json.loads((self.root / "engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json").read_text(encoding="utf-8"))
        next_item = plan.get("next")
        if not isinstance(next_item, str) or not next_item.strip():
            raise ValueError("master plan has no declared next macrodelivery")
        deferred = tuple(item.removeprefix("DEFERRED: ").strip() for item in plan.get("backlog", []) if str(item).startswith("DEFERRED:"))
        return SelectionResult(next_item, "selected from active master plan; external gates remain authoritative", deferred)
