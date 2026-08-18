import pytest
from design.steel.panel_zone import *
@pytest.mark.parametrize("i",range(120))
def test_panel(i):
    assert PanelZoneEngine().design(50,50,20,2,100).ratio>0
