import pytest
from design.steel.column_splice import *
@pytest.mark.parametrize("i",range(120))
def test_column_splice(i):
    assert ColumnSpliceEngine().design(100,300,20,100,10,80).passed
