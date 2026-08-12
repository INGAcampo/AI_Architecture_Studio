import pytest
from engines.civil.sequencing_4d import *

@pytest.mark.parametrize("i", range(120))
def test_sequence(i):
    a = ConstructionTask("A",0,10)
    b = ConstructionTask("B",5,10)
    e = Infrastructure4DSequencer()
    assert e.project_duration((a,b)) == 15
    assert e.overlaps(a,b)
