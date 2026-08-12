import pytest
from design.steel.column_slenderness import ColumnSlendernessEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_slenderness(i):
    pr=SteelProfileRepository(); mr=SteelMaterialRepository(); seed_default_catalog(pr,mr)
    p=pr.get("W14X38")
    r=ColumnSlendernessEngine().calculate(3.0,3.0,p)
    assert r.maximum>0
    assert r.minor>=r.major
