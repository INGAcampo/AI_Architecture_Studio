import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.delamination_initiation import DelaminationInitiationEngine
    assert DelaminationInitiationEngine().quadratic(10,0,20,10)==pytest.approx(.25)
