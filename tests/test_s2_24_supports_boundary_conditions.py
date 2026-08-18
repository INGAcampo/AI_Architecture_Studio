import pytest
from engines.structural.supports import *
@pytest.mark.parametrize("index", range(120))
def test_supports(index):
    engine=SupportEngine()
    support=Support(f"S{index}","N1",SupportKind.FIXED,rz=index%2==0)
    engine.add(support)
    assert len(engine.for_node("N1")) == 1
    assert 5 <= support.restrained_dofs <= 6
