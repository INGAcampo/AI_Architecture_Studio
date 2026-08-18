import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_domain import GPUDevice
    assert GPUDevice('0','G','x',100,4).compute_units==4
