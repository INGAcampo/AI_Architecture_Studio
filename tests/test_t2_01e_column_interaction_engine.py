import pytest
from design.steel.column_interaction import ColumnInteractionEngine

@pytest.mark.parametrize("i", range(120))
def test_interaction(i):
    r=ColumnInteractionEngine().calculate(200,1000,50,200,10,100)
    assert r.interaction_ratio>0
    assert r.equation in {"H1-1a","H1-1b"}
