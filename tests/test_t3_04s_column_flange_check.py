import pytest
from design.steel.column_flange_check import *
@pytest.mark.parametrize("i",range(120))
def test_flange(i):
    assert ColumnFlangeCheckEngine().design(100,300,250,280).passed
