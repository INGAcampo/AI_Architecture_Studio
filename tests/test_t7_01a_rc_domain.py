import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rc_domain import RCBeamInput
    assert RCBeamInput('B',300,500,450,28,420,1,1).width==300
