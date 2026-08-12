import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_library.en_s235 import material
    assert material().fy_mpa>0
