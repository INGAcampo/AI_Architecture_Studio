from standards_engine.contracts import EvaluationContext,Rule,RuleSet
from standards_engine.engine import evaluate_rule_set


def test_rule_engine_is_deterministic():
    rules=RuleSet(
        "demo",
        (
            Rule(
                "R1",
                "Positive span",
                lambda c: c.values["span_m"]>0,
                source_reference="DEMO-NOT-A-CODE",
            ),
            Rule(
                "R2",
                "Finite load",
                lambda c: abs(c.values["load_n"])<1e12,
                severity="WARNING",
                source_reference="DEMO-NOT-A-CODE",
            ),
        ),
    )
    result=evaluate_rule_set(
        rules,
        EvaluationContext({"span_m":6.0,"load_n":10000.0}),
    )
    assert tuple(item.passed for item in result)==(True,True)


def test_rule_exception_fails_closed_with_trace():
    rules=RuleSet(
        "demo",
        (
            Rule(
                "R1",
                "Needs missing key",
                lambda c: c.values["missing"]>0,
            ),
        ),
    )
    result=evaluate_rule_set(rules,EvaluationContext({}))
    assert result[0].passed is False
    assert "KeyError" in result[0].error


def test_duplicate_rule_id_is_rejected():
    rules=RuleSet(
        "bad",
        (
            Rule("X","One",lambda c:True),
            Rule("X","Two",lambda c:True),
        ),
    )
    failed=False
    try:
        rules.validate()
    except ValueError:
        failed=True
    assert failed is True
