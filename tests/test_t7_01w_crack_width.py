import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.crack_width import CrackWidthEngine
    assert CrackWidthEngine().estimate(200,150,40)>0
