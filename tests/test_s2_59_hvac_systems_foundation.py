import pytest
from engines.structural.hvac import *

@pytest.mark.parametrize("index", range(120))
def test_hvac(index):
    system = HvacSystem(
        f"H{index}",
        list(HvacSystemType)[index % len(HvacSystemType)],
        100 + index,
        3.0,
    )
    engine = HvacSystemEngine()
    load = 50 + index * 0.1
    assert engine.electrical_power(system, load) == pytest.approx(load / 3.0)
    assert engine.is_adequate(system, load)
