import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.penalty_contact import PenaltyContactEngine
    assert PenaltyContactEngine().pressure(-.01,1000)==pytest.approx(10)
