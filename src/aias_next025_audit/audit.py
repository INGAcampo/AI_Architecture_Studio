from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AuditResult:
    valid: bool
    current: str | None
    next_item: str | None
    deferred_items: tuple[str, ...]
    issues: tuple[str, ...]


class RoadmapIntegrityAudit:
    def __init__(self, plan_path: str | Path):
        self.path = Path(plan_path)

    def run(self) -> AuditResult:
        if not self.path.exists():
            return AuditResult(False, None, None, (), ("master plan absent",))
        plan = json.loads(self.path.read_text(encoding="utf-8"))
        current, next_item = plan.get("current"), plan.get("next")
        backlog = tuple(str(item) for item in plan.get("backlog", []))
        deferred = tuple(item for item in backlog if item.startswith("DEFERRED:"))
        issues = []
        if not current or not next_item:
            issues.append("current and next are required")
        if any(item == next_item for item in deferred):
            issues.append("next item is explicitly deferred")
        return AuditResult(not issues, current, next_item, deferred, tuple(issues))
