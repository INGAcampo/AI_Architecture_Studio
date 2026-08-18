import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.dof_manager import GlobalDofManager
    m=GlobalDofManager();m.register('N',('UX','UY'));assert m.index('N','UY')==1
