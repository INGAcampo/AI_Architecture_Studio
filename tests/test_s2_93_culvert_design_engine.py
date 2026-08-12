import pytest
from engines.civil.culverts import *
@pytest.mark.parametrize("i",range(120))
def test_culvert(i):
    c=CircularCulvert(f"C{i}",1.2,0.01,0.013);e=CulvertDesignEngine()
    assert e.area(c)>0 and e.capacity(c)>0
