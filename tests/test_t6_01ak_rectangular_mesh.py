import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.rectangular_mesh import RectangularMesh
    n,e=RectangularMesh().generate(2,1,2,1);assert len(n)==6 and len(e)==2
