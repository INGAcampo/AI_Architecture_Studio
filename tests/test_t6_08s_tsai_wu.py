import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.tsai_wu import TsaiWuEngine
    assert isinstance(TsaiWuEngine().index(10,5,2,100,80,50,40,30),float)
