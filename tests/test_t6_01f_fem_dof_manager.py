import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_dof_manager import FemDofManager
    m=FemDofManager();m.register('N',('UX','UY'));assert m.index('N','UY')==1
