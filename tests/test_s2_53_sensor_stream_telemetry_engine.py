import pytest
from engines.structural.telemetry import *

@pytest.mark.parametrize("index", range(120))
def test_telemetry(index):
    engine = SensorStreamEngine()
    first = TelemetrySample(f"S{index}", f"A{index}", "temperature", 20 + index, 1.0)
    second = TelemetrySample(f"S{index}", f"A{index}", "temperature", 22 + index, 2.0)
    engine.publish(second)
    engine.publish(first)
    assert engine.latest(first.asset_id, first.metric) is second
    assert engine.window(first.asset_id, first.metric, 0.5, 1.5) == (first,)
    assert engine.average(first.asset_id, first.metric) == pytest.approx(21 + index)
