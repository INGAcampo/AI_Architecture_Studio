from __future__ import annotations
from collections import OrderedDict
from typing import Iterable

from .rule import Rule


class RuleRegistry:
    def __init__(self) -> None:
        self._rules: "OrderedDict[str, Rule]" = OrderedDict()

    def register(self, rule: Rule, *, replace: bool = False) -> None:
        if not rule.rule_id.strip():
            raise ValueError("rule_id es obligatorio")
        if rule.rule_id in self._rules and not replace:
            raise ValueError(f"Regla duplicada: {rule.rule_id}")
        self._rules[rule.rule_id] = rule

    def unregister(self, rule_id: str) -> Rule:
        try:
            return self._rules.pop(rule_id)
        except KeyError as exc:
            raise KeyError(f"Regla inexistente: {rule_id}") from exc

    def get(self, rule_id: str) -> Rule:
        try:
            return self._rules[rule_id]
        except KeyError as exc:
            raise KeyError(f"Regla inexistente: {rule_id}") from exc

    def all(self) -> tuple[Rule, ...]:
        return tuple(self._rules.values())

    def enabled(self) -> tuple[Rule, ...]:
        return tuple(rule for rule in self._rules.values() if rule.enabled)

    def by_tag(self, tag: str) -> tuple[Rule, ...]:
        return tuple(rule for rule in self._rules.values() if tag in rule.tags)

    def clear(self) -> None:
        self._rules.clear()

    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterable[Rule]:
        return iter(self._rules.values())
