import pytest
from design.steel.column_domain import ColumnEndCondition
from design.steel.effective_length import EffectiveLengthEngine

@pytest.mark.parametrize("i", range(120))
def test_effective_length(i):
    e=EffectiveLengthEngine()
    assert e.factor(ColumnEndCondition.PINNED_PINNED)==pytest.approx(1.0)
    assert e.effective_length(4,ColumnEndCondition.FIXED_FIXED).value==pytest.approx(2.6)
