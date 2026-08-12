from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .issue import Issue, IssueSeverity


@dataclass(frozen=True, slots=True)
class RuleContext:
    project: Any
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RuleResult:
    issues: tuple[Issue, ...] = ()
    inspected_count: int = 0
    skipped_count: int = 0

    @property
    def has_issues(self) -> bool:
        return bool(self.issues)


class Rule(ABC):
    rule_id: str = "rule.base"
    name: str = "Base Rule"
    description: str = ""
    default_severity: IssueSeverity = IssueSeverity.WARNING
    enabled: bool = True
    tags: tuple[str, ...] = ()

    def applies_to(self, element: Any, context: RuleContext) -> bool:
        return True

    @abstractmethod
    def evaluate(self, element: Any, context: RuleContext) -> Iterable[Issue]:
        raise NotImplementedError

    def run_element(self, element: Any, context: RuleContext) -> RuleResult:
        if not self.enabled or not self.applies_to(element, context):
            return RuleResult(skipped_count=1)
        issues = tuple(self.evaluate(element, context))
        return RuleResult(issues=issues, inspected_count=1)
