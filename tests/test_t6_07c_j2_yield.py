import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.j2_yield import J2YieldEngine
    assert J2YieldEngine().equivalent_stress((10,0,0,0,0,0))==pytest.approx(10)
