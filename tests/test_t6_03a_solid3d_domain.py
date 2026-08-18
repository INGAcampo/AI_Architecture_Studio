import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.solid3d_domain import SolidNode
    assert SolidNode('N',(0,0,0)).coordinates==(0,0,0)
