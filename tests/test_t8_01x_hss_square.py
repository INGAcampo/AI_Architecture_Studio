import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_library.hss_square import sample
    assert sample().area_mm2>0
