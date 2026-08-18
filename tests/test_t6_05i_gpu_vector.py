import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_vector import GPUVectorEngine
    assert GPUVectorEngine().add((1,2),(3,4))==(4,6)
