import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_ai_optimizer import GPUAIOptimizer
    assert GPUAIOptimizer().recommend(5000,8_000_000_000).backend=='gpu'
