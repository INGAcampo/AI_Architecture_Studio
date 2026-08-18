import pytest
from types import SimpleNamespace
from design.steel.base_plate_domain import BasePlateDemand
from design.steel.foundation_transfer import *
@pytest.mark.parametrize("i",range(120))
def test_transfer(i):
    r=FoundationTransferEngine().calculate(BasePlateDemand(500e3,20e3,10e3,5e3,2e3),SimpleNamespace(passed=True))
    assert r.transfer_complete
