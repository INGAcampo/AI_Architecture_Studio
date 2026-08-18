import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_domain import FemElement
    from analysis.fem.element_repository import ElementRepository
    r=ElementRepository();r.add(FemElement('E',('N1','N2'),'M'));assert r.get('E').material_id=='M'
