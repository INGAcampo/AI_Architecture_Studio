import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_vertical_slice import GPUVerticalSlice
    r=GPUVerticalSlice().run(((4,0),(0,9)),(8,18));assert r.run.converged and r.optimization.backend=='gpu'
