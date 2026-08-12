import pytest
from engines.structural.conflicts import *
@pytest.mark.parametrize("index",range(120))
def test_conflicts(index):
    r=ConflictResolver();c=ChangeSet(f"O{index}",{"x":index},{"x":index+1})
    assert r.conflicts(c)==("x",)
    assert r.resolve(c,ConflictResolution.MERGED)["x"]==index
