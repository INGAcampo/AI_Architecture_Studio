import pytest
from engines.civil.stormwater import *

@pytest.mark.parametrize("index", range(120))
def test_stormwater(index):
    catchment = Catchment(
        f"C{index}", 2.0 + index*0.01, 0.75, 90.0
    )
    engine = StormwaterDrainageEngine()
    flow = engine.rational_peak_flow(catchment)
    assert flow > 0
    assert engine.detention_volume(flow, flow*0.6, 1800) > 0
