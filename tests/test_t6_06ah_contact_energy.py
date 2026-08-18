import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_energy import ContactEnergyEngine
    assert ContactEnergyEngine().penalty_energy(.01,1000)==pytest.approx(.05)
