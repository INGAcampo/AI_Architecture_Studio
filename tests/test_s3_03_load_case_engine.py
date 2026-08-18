import pytest
from engines.structural.systems.load_cases import *

@pytest.mark.parametrize("i",range(120))
def test_load_case(i):
    e=LoadCaseEngine()
    d=LoadCase(f"D{i}","Dead",LoadCategory.DEAD,1.0,{})
    e.add(d)
    assert e.get(f"D{i}").self_weight_multiplier==1.0
    assert e.by_category(LoadCategory.DEAD)==(d,)
