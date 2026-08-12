import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.coulomb_friction import CoulombFrictionEngine
    assert CoulombFrictionEngine().state(2,10,.3)=='stick'
