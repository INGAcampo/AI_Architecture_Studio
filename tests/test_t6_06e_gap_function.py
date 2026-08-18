import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.gap_function import GapFunctionEngine
    assert GapFunctionEngine().normal_gap((0,-1),(0,0),(0,1))==-1
