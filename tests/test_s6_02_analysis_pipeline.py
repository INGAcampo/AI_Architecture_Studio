import pytest
from engines.analysis.pipeline import *

@pytest.mark.parametrize("i",range(120))
def test_pipeline(i):
    p=AnalysisPipeline()
    r=p.run((("a",lambda c:2),("b",lambda c:c["a"]*3)),{})
    assert r.completed
    assert r.stages[-1].output==6
