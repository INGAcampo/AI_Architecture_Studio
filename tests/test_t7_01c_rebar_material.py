import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rebar_material import RebarMaterial
    assert RebarMaterial('S',420).fy==420
