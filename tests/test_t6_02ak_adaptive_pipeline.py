import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.adaptive_pipeline import AdaptivePipeline
    r=AdaptivePipeline().run((.1,.4,.2),(1,1,1),.05)
    assert r.marked_elements==(1,)
