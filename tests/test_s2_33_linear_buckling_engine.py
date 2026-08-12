import pytest
from engines.structural.buckling import *

@pytest.mark.parametrize("index", range(120))
def test_buckling(index):
    engine = LinearBucklingEngine()
    load = engine.euler_load(200e9, 1e-5 + index*1e-7, 3.0)
    mode = BucklingMode(index + 1, load)
    assert engine.critical_mode((mode,)) is mode
    assert load > 0
