import pytest
from types import SimpleNamespace
from design.steel.connection_ai_advisor import *
@pytest.mark.parametrize("i",range(120))
def test_ai(i):
    r=SimpleNamespace(passed=True,governing_check="shear")
    assert "cumple" in ConnectionAIAdvisor().advise(r).summary
