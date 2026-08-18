import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.flexural_strength import FlexuralStrengthEngine
    assert FlexuralStrengthEngine().nominal_moment(1000,420,300,500,28)>0
