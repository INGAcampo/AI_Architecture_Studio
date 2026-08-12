import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.pmm_interaction import PMMInteractionEngine
    assert PMMInteractionEngine().ratio(1,10,1,10,1,10)==pytest.approx(.3)
