import pytest
from engines.structural.load_codes import *

@pytest.mark.parametrize("index", range(120))
def test_load_codes(index):
    engine = LoadCodeEngine()
    params = WindParameters(30 + index*0.1, 1.0, 1.0)
    assert engine.wind_pressure(params) > 0
    assert engine.seismic_base_shear(1000 + index, 0.1) == pytest.approx((1000 + index)*0.1)
