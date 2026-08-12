import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.hashin import HashinEngine
    assert HashinEngine().fiber_tension(10,0,100,50)==pytest.approx(.01)
