import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_domain import FemNode
    from analysis.fem.node_repository import NodeRepository
    r=NodeRepository();r.add(FemNode('N',(0,0)));assert r.get('N').node_id=='N'
