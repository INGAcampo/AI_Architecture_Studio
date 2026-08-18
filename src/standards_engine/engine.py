from __future__ import annotations

from .contracts import EvaluationContext,Rule,RuleOutcome,RuleSet


def evaluate_rule(rule:Rule,context:EvaluationContext)->RuleOutcome:
    rule.validate()
    try:
        passed=bool(rule.predicate(context))
        return RuleOutcome(
            rule_id=rule.rule_id,
            passed=passed,
            severity=rule.severity,
            source_reference=rule.source_reference,
            error=None,
        )
    except Exception as exc:
        return RuleOutcome(
            rule_id=rule.rule_id,
            passed=False,
            severity=rule.severity,
            source_reference=rule.source_reference,
            error=f"{type(exc).__name__}: {exc}",
        )


def evaluate_rule_set(ruleset:RuleSet,context:EvaluationContext):
    ruleset.validate()
    return tuple(evaluate_rule(rule,context) for rule in ruleset.rules)
