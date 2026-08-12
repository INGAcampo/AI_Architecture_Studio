import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.longitudinal_rebar_ratio import LongitudinalRebarRatioEngine
    assert LongitudinalRebarRatioEngine().acceptable(.02)
