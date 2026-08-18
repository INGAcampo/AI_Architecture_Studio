import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.structured_quad_mesh import StructuredQuadMeshGenerator
    n,e=StructuredQuadMeshGenerator().generate(2,1,2,1)
    assert len(n)==6 and len(e)==2
