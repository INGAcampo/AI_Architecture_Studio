import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.isotropic_hardening import IsotropicHardeningLaw
    assert IsotropicHardeningLaw().yield_stress(250,1000,.01)==260
