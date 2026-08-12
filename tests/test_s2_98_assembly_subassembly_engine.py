import pytest
from engines.civil.assemblies import *

@pytest.mark.parametrize("i", range(120))
def test_assembly(i):
    a = Assembly(f"A{i}", (
        Subassembly("L", 3.5, -0.02, "LANE"),
        Subassembly("S", 1.5, -0.04, "SHOULDER"),
    ))
    e = AssemblyEngine()
    assert e.total_width(a) == 5
    assert e.codes(a) == ("LANE", "SHOULDER")
