import pytest
from design.steel.column_domain import *

@pytest.mark.parametrize("i", range(120))
def test_column_domain(i):
    c=SteelColumn(
        f"C{i}","W14X38","ASTM_A992",3.5,
        ColumnEndCondition.PINNED_PINNED,
        ColumnEndCondition.FIXED_FIXED,
        SteelColumnDemand(500e3,20e3,5e3)
    )
    assert c.length==pytest.approx(3.5)
    assert EffectiveLength(3.5,0.65).value==pytest.approx(2.275)
