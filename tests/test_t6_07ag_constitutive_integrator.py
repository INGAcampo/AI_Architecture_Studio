import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.constitutive_integrator import ConstitutiveIntegrator
    assert ConstitutiveIntegrator().integrate_j2((350,0,0,0,0,0),80000,250).yielded
