import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_domain import GPUDevice
    from analysis.gpu.device_manager import GPUDeviceManager
    assert GPUDeviceManager((GPUDevice('0','A','x',1,2),GPUDevice('1','B','x',1,4))).best().name=='B'
