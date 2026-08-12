import pytest
from engines.structural.systems.clash_detection import *

@pytest.mark.parametrize("i",range(120))
def test_clash(i):
    e=StructuralClashDetection()
    a=BoundingBox("A",(0,0,0),(2,2,2))
    b=BoundingBox("B",(1,1,1),(3,3,3))
    c=BoundingBox("C",(4,4,4),(5,5,5))
    assert e.detect((a,b,c))==(StructuralClash("A","B"),)
