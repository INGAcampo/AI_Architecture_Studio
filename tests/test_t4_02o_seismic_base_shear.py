import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.seismic_base_shear import SeismicBaseShearEngine
    assert SeismicBaseShearEngine().calculate(.2,1000)==200
