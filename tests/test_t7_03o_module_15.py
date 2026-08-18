import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_slabs.module_15 import Engine
    assert Engine().calculate(1,2,3)==6
    assert Engine().utilization(5,10)==pytest.approx(.5)
