import pytest
from engines.ai.adaptive_components import *
@pytest.mark.parametrize("i",range(120))
def test_adaptive(i):
    c=AdaptiveComponent(f"C{i}",(AdaptivePoint("A",0,0),AdaptivePoint("B",2,0)))
    e=AdaptiveComponentEngine();assert e.centroid(c)==(1,0,0)
    c2=e.move_point(c,"B",4,0);assert e.centroid(c2)==(2,0,0)
