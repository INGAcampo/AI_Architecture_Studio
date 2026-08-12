import pytest
from design.steel.brace_vertical_slice import BraceStabilityVerticalSlice
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_vertical_slice(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    r=BraceStabilityVerticalSlice(pr,mr).run(f"BR{i}","HSS200X200X8","ASTM_A992",4,-200e3,10e6,0.01,500e3,3.5)
    assert r.design_result.unity_ratio>=0
    assert "# Steel Brace System Report" in r.report.markdown
