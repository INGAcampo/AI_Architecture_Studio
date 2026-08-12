import pytest
from design.steel.column_web_check import *
@pytest.mark.parametrize("i",range(120))
def test_web(i):
    assert ColumnWebCheckEngine().design(100,250,220,240).passed
