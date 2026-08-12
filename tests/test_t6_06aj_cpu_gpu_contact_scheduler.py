import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.cpu_gpu_contact_scheduler import CPUGPUContactScheduler
    assert CPUGPUContactScheduler().choose(6000)=='gpu'
