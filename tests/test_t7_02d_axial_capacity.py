import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.axial_capacity import AxialCapacityEngine
    assert AxialCapacityEngine().nominal(30,200000,4000,420)>0
