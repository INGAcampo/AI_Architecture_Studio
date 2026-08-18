import pytest
from engines.structural.platform.connections import *

@pytest.mark.parametrize("i",range(120))
def test_connections(i):
    e=StructuralConnectionEngine()
    c=StructuralConnection(f"J{i}","N1",("C1","B1"),ConnectionType.RIGID)
    e.add(c)
    assert e.for_member("C1")== (c,)
    assert e.validate(c)==()
