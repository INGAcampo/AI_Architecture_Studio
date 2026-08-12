import pytest
from engines.structural.combinations import *
@pytest.mark.parametrize("index", range(120))
def test_combinations(index):
    engine=CombinationEngine()
    combo=LoadCombination(f"C{index}",(LoadFactor("D",1.2),LoadFactor("L",1.6)))
    engine.add(combo)
    assert engine.evaluate(combo.combination_id,{"D":index,"L":2}) == pytest.approx(1.2*index+3.2)
