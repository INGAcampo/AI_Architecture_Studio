import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.concrete_stress_strain import ConcreteStressStrainModel
    assert ConcreteStressStrainModel().stress(.001,30e6)>0
