import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.memory_manager import GPUMemoryManager
    m=GPUMemoryManager(100);m.allocate(40);m.release(10);assert m.used==30
