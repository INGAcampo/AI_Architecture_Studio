import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.uniaxial_flexure import UniaxialFlexureEngine
    assert UniaxialFlexureEngine().capacity(1e6,500)>0
