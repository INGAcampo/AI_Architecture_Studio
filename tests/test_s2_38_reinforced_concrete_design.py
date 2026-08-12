import pytest
from engines.structural.concrete_design import *

@pytest.mark.parametrize("index", range(120))
def test_concrete_design(index):
    section = ConcreteSection(f"C{index}", 0.30, 0.50 + index*0.001, 30e6, 420e6, 0.0015)
    engine = ReinforcedConcreteDesignEngine()
    assert engine.nominal_moment(section) > 0
    assert engine.design_strength(section) > 0
    assert engine.reinforcement_ratio(section) > 0
