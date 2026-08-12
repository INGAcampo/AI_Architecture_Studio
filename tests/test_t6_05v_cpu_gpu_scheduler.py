import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.cpu_gpu_scheduler import CPUGPUScheduler
    assert CPUGPUScheduler().choose(5000)=='gpu'
