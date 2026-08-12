import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.transient_domain import TransientStep
    assert TransientStep(0,1,2,3).velocity==2
