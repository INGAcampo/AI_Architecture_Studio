import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.augmented_lagrangian import AugmentedLagrangianEngine
    assert AugmentedLagrangianEngine().update_multiplier(0,-.01,1000)==pytest.approx(10)
