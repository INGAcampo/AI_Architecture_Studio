import pytest
from engines.structural.clashes import *
@pytest.mark.parametrize("index",range(120))
def test_clash_detection(index):
    d=ClashDetector();a=BoundingBox(0,0,0,1,1,1);b=BoundingBox(.5,.5,.5,1.5+index*.001,1.5,1.5)
    assert d.detect(f"A{index}",a,f"B{index}",b).kind is ClashKind.HARD
