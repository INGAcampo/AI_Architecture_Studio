import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_result_pipeline import GPUResultPipeline
    assert GPUResultPipeline().normalize((0,5,10))==pytest.approx((0,.5,1))
