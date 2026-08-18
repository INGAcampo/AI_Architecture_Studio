from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Iterable

from .issue import Issue, IssueSeverity
from .registry import RuleRegistry
from .rule import Rule, RuleContext


@dataclass(frozen=True, slots=True)
class RuleEngineStatistics:
    runs: int
    inspected_elements: int
    evaluated_rules: int
    issue_count: int
    by_severity: dict[str, int]
    duration_seconds: float


class RuleEngine:
    def __init__(self, registry: RuleRegistry | None = None) -> None:
        self.registry = registry or RuleRegistry()
        self._issues: list[Issue] = []
        self._runs = 0
        self._inspected = 0
        self._evaluated_rules = 0
        self._duration = 0.0

    def _elements_from_project(self, project: Any) -> tuple[Any, ...]:
        if hasattr(project, "elements"):
            return tuple(project.elements)
        if isinstance(project, dict) and "elements" in project:
            return tuple(project["elements"])
        if isinstance(project, Iterable) and not isinstance(project, (str, bytes, dict)):
            return tuple(project)
        raise TypeError("El proyecto no expone una colección de elementos")

    def run(self, project: Any, *, metadata: dict | None = None) -> tuple[Issue, ...]:
        start = perf_counter()
        context = RuleContext(project=project, metadata=metadata or {})
        elements = self._elements_from_project(project)
        new_issues: list[Issue] = []

        for element in elements:
            for rule in self.registry.enabled():
                result = rule.run_element(element, context)
                self._inspected += result.inspected_count
                self._evaluated_rules += result.inspected_count
                new_issues.extend(result.issues)

        self._issues.extend(new_issues)
        self._runs += 1
        self._duration += perf_counter() - start
        return tuple(new_issues)

    def run_element(
        self,
        element: Any,
        *,
        project: Any = None,
        metadata: dict | None = None,
    ) -> tuple[Issue, ...]:
        context = RuleContext(project=project, metadata=metadata or {})
        issues: list[Issue] = []
        for rule in self.registry.enabled():
            result = rule.run_element(element, context)
            self._inspected += result.inspected_count
            self._evaluated_rules += result.inspected_count
            issues.extend(result.issues)
        self._issues.extend(issues)
        self._runs += 1
        return tuple(issues)

    def run_rule(
        self,
        rule: Rule | str,
        project: Any,
        *,
        metadata: dict | None = None,
    ) -> tuple[Issue, ...]:
        selected = self.registry.get(rule) if isinstance(rule, str) else rule
        context = RuleContext(project=project, metadata=metadata or {})
        issues: list[Issue] = []
        for element in self._elements_from_project(project):
            result = selected.run_element(element, context)
            self._inspected += result.inspected_count
            self._evaluated_rules += result.inspected_count
            issues.extend(result.issues)
        self._issues.extend(issues)
        self._runs += 1
        return tuple(issues)

    def issues(
        self,
        *,
        minimum_severity: IssueSeverity | None = None,
    ) -> tuple[Issue, ...]:
        if minimum_severity is None:
            return tuple(self._issues)
        return tuple(
            issue for issue in self._issues
            if issue.severity >= minimum_severity
        )

    def statistics(self) -> RuleEngineStatistics:
        by_severity = {severity.name: 0 for severity in IssueSeverity}
        for issue in self._issues:
            by_severity[issue.severity.name] += 1
        return RuleEngineStatistics(
            runs=self._runs,
            inspected_elements=self._inspected,
            evaluated_rules=self._evaluated_rules,
            issue_count=len(self._issues),
            by_severity=by_severity,
            duration_seconds=self._duration,
        )

    def clear(self) -> None:
        self._issues.clear()
        self._runs = 0
        self._inspected = 0
        self._evaluated_rules = 0
        self._duration = 0.0
