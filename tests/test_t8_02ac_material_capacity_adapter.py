import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.material_capacity_adapter import MaterialCapacityAdapter
    class M:
        fy_mpa=345.0
    assert MaterialCapacityAdapter().yield_strength_mpa(M())==345.0
