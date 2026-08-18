import pytest
from design.steel.bolt_group import BoltPoint
from design.steel.bolt_vertical_slice import BoltConnectionVerticalSlice

@pytest.mark.parametrize("i", range(120))
def test_vertical_slice(i):
    pts=(BoltPoint("B1",-0.05,-0.05),BoltPoint("B2",0.05,-0.05),BoltPoint("B3",0.05,0.05),BoltPoint("B4",-0.05,0.05))
    r=BoltConnectionVerticalSlice().run(pts,100e3,20e3,5e3,10e3)
    assert len(r.bolt_results)==4
    assert "# Bolt Connection Design Report" in r.report_markdown
