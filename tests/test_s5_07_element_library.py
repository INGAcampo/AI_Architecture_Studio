import pytest
from engines.fem.library import *
from engines.fem.truss import TrussElement

@pytest.mark.parametrize("i",range(120))
def test_library(i):
    lib=FiniteElementLibrary()
    e=TrussElement(f"T{i}",("N1","N2"),(0,0,0),(1,0,0),0.01,200e9)
    lib.register(e)
    assert lib.get(f"T{i}") is e
    assert lib.by_type("TrussElement")== (e,)
