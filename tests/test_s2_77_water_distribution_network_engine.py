import pytest
from engines.civil.water_network import *

@pytest.mark.parametrize("index", range(120))
def test_water_network(index):
    pipe = WaterPipe(
        f"P{index}", 100 + index, 0.20 + index*0.0005, 130.0, 0.02
    )
    engine = WaterDistributionEngine()
    assert pipe.area > 0
    assert pipe.velocity > 0
    assert engine.head_loss_hazen_williams(pipe) > 0
    assert engine.pressure_drop(pipe) > 0
