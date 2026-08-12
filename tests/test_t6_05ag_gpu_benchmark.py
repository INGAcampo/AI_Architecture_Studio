import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_benchmark import GPUBenchmarkEngine
    assert GPUBenchmarkEngine().speedup(4,2)==2
