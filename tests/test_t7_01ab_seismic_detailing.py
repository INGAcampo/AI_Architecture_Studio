import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.seismic_detailing import SeismicDetailingEngine
    assert SeismicDetailingEngine().stirrup_spacing_limit(500,10)==60
