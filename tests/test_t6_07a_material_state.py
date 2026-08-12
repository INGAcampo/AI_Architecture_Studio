import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.material_state import MaterialState
    assert not MaterialState((1,)*6,(0,)*6,0,0,False).yielded
