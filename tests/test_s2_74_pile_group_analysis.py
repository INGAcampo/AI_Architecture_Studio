import pytest
from engines.geotechnical.pile_groups import *
@pytest.mark.parametrize("i",range(120))
def test_group(i):
    g=PileGroup(f"G{i}",4,500+i,.85,25000); e=PileGroupAnalysis()
    assert e.group_capacity(g)>500 and sum(e.distribute_load(g,1000))==pytest.approx(1000)
