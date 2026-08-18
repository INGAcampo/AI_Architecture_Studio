import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.energy_balance import EnergyBalanceEngine
    assert EnergyBalanceEngine().error(10,3,4,3)==pytest.approx(0)
