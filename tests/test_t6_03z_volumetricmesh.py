import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.volumetricmesh import VolumetricMeshEngine
    assert len(VolumetricMeshEngine().unit_tetra()[0])==4
