import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_library.hss_rectangular import sample
    assert sample().area_mm2>0
