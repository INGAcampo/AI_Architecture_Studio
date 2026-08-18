import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_domain import FemNode
    assert FemNode('N',(0,0)).node_id=='N'
