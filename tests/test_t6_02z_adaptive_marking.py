import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.adaptive_marking import AdaptiveMarkingEngine
    assert AdaptiveMarkingEngine().mark((.1,.5,.2),.34)==(1,)
