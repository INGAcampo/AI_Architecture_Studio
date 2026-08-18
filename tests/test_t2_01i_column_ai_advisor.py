import pytest
from design.steel.column_ai_advisor import SteelColumnAIAdvisor
from design.steel.column_domain import SteelColumnDesignResult,BucklingAxis

@pytest.mark.parametrize("i", range(120))
def test_column_ai(i):
    r=SteelColumnDesignResult(f"C{i}",50,80,BucklingAxis.MINOR,1e6,0.4,0.2,0.1,0.58,0.58,True,"interaction")
    a=SteelColumnAIAdvisor().explain(r)
    assert "cumple" in a.message and "minor" in a.message
