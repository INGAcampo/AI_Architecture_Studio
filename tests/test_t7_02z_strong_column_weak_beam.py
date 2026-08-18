import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.strong_column_weak_beam import StrongColumnWeakBeamEngine
    assert StrongColumnWeakBeamEngine().passes((400,400),(300,300))
