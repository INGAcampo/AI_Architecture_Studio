import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.tsai_hill import TsaiHillEngine
    assert TsaiHillEngine().index(10,0,0,100,100,100)==pytest.approx(.01)
