import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.bar_selection import BarSelectionEngine
    assert BarSelectionEngine().select(1000,(200,300)) is not None
