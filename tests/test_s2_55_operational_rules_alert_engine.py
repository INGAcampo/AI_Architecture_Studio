import pytest
from engines.structural.alerts import *

@pytest.mark.parametrize("index", range(120))
def test_alerts(index):
    engine = AlertEngine()
    rule = OperationalRule(
        f"R{index}",
        "temperature",
        Comparison.GREATER_EQUAL,
        30.0,
        AlertSeverity.WARNING,
    )
    value = 30.0 + index
    alert = engine.evaluate(rule, f"A{index}", value)
    assert alert is not None
    assert alert.value == value
    assert alert.severity is AlertSeverity.WARNING
