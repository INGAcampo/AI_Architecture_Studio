from __future__ import annotations

from dataclasses import dataclass,field
from typing import Any,Callable


@dataclass(frozen=True)
class EvaluationContext:
    values: dict[str,Any]


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    predicate: Callable[[EvaluationContext],bool]
    severity: str = "ERROR"
    source_reference: str | None = None

    def validate(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if self.severity not in {"INFO","WARNING","ERROR"}:
            raise ValueError("unsupported severity")


@dataclass(frozen=True)
class RuleOutcome:
    rule_id: str
    passed: bool
    severity: str
    source_reference: str | None
    error: str | None = None


@dataclass(frozen=True)
class RuleSet:
    ruleset_id: str
    rules: tuple[Rule,...] = field(default_factory=tuple)

    def validate(self) -> None:
        if not self.ruleset_id.strip():
            raise ValueError("ruleset_id must not be empty")
        ids=[rule.rule_id for rule in self.rules]
        if len(ids)!=len(set(ids)):
            raise ValueError("duplicate rule_id")
