import pytest
from engines.structural.systems.load_combinations import *

@pytest.mark.parametrize("i",range(120))
def test_combination(i):
    c=LoadCombination(f"C{i}","1.2D+1.6L",(LoadFactor("D",1.2),LoadFactor("L",1.6)))
    e=LoadCombinationEngine()
    assert e.evaluate(c,{"D":100,"L":50})==pytest.approx(200)
    assert e.validate(c,{"D","L"})==()
