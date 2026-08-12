import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.cpu_gpu_transient_scheduler import CPUGPUTransientScheduler
    assert CPUGPUTransientScheduler().choose(1000,200)=='gpu'
