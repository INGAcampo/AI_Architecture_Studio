import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.torsion_design import TorsionDesignEngine
    assert TorsionDesignEngine().required_transverse_ratio(1e6,.75,1e5,420)>0
