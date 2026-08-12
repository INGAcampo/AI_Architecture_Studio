import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.peak_response import PeakResponseEngine
    assert PeakResponseEngine().peak((-3,2))==3
