import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.green_lagrange_strain import GreenLagrangeStrainEngine
    assert GreenLagrangeStrainEngine().one_dimensional(1)==0
