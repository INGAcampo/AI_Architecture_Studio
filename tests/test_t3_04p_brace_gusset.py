import pytest
from design.steel.brace_gusset import *
@pytest.mark.parametrize("i",range(120))
def test_gusset(i):
    assert BraceGussetEngine().design(100,250,200,220).passed
