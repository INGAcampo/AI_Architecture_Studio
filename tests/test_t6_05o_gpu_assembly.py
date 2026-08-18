import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_assembly import GPUAssemblyEngine
    assert GPUAssemblyEngine().assemble((((1,-1),(-1,1)),),((0,1),),2)[0][0]==1
