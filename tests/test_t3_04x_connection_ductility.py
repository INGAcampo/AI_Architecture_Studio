import pytest
from design.steel.connection_ductility import *
@pytest.mark.parametrize("i",range(120))
def test_ductility(i):
    assert ConnectionDuctilityEngine().check(.04,.02).passed
