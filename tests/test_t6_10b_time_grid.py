import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.time_grid import TimeGridEngine
    assert TimeGridEngine().build(0,.2,.1)==pytest.approx((0,.1,.2))
