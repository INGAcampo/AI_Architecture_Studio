import pytest
from engines.geotechnical.spread_footings import *
@pytest.mark.parametrize("i",range(120))
def test_footing(i):
    f=SpreadFooting(f"F{i}",3,3,900+i,250); e=SpreadFootingDesign()
    assert e.bearing_ok(f)
