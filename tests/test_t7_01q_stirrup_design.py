import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.stirrup_design import StirrupDesignEngine
    assert StirrupDesignEngine().required_av_over_s(200000,.75,100000,420,500)>0
