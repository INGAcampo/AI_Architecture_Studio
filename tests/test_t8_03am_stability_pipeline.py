import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.stability_pipeline import StabilityPipeline
    assert StabilityPipeline().run_demo()[2].status=='PASS'
