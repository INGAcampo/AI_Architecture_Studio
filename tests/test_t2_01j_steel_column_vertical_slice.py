import pytest
from design.steel.column_vertical_slice import SteelColumnVerticalSlice
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_column_vertical_slice(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    flow=SteelColumnVerticalSlice(pr,mr)
    r=flow.run(f"C{i}","W14X38","ASTM_A992",3.5,350e3,20e3,5e3)
    assert r.column.member_id==f"C{i}"
    assert r.design_result.unity_ratio>=0
    assert "# Steel Column Design" in r.report.markdown
