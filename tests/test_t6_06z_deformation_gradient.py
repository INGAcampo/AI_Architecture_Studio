import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.deformation_gradient import DeformationGradientEngine
    assert DeformationGradientEngine().one_dimensional(2,1)==2
