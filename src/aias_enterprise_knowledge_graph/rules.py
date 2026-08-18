"""Explicit allowlisted inference rules for the enterprise graph."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InferenceRule:
    """Declare one approved two-hop relationship inference."""
    rule_id: str
    left_relation: str
    right_relation: str
    inferred_relation: str
    approved_by: str


class RuleRegistry:
    """Store only explicitly approved inference rules."""
    def __init__(self, rules: list[InferenceRule] | None = None):
        self._rules = {rule.rule_id: rule for rule in (rules or [])}

    def approved(self, rule_id: str) -> InferenceRule:
        """Return an approved rule or reject an unregistered rule identifier."""
        try:
            rule = self._rules[rule_id]
        except KeyError as exc:
            raise ValueError("unapproved_inference_rule") from exc
        if not rule.approved_by:
            raise ValueError("unapproved_inference_rule")
        return rule
