import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.material_history import MaterialHistory
    h=MaterialHistory();h.add(3);assert h.latest()==3
