import pytest
from design.steel.block_shear import *
@pytest.mark.parametrize("i",range(120))
def test_block(i):
    assert BlockShearEngine().calculate(.003,.0025,.001,250e6,400e6,100e3).design_capacity>0
