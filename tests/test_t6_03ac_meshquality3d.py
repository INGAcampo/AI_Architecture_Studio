import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.meshquality3d import MeshQuality3DEngine
    assert MeshQuality3DEngine().calculate(1/6)==pytest.approx(1)
