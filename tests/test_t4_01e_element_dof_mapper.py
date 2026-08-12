import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.dof_manager import GlobalDofManager
    from analysis.matrix.element_dof_mapper import ElementDofMapper
    m=GlobalDofManager();m.register('N',('UX',));assert ElementDofMapper().map(m,('N',),('UX',))==(0,)
