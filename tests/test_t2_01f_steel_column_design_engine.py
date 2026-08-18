import pytest
from design.steel.column_domain import *
from design.steel.column_design_engine import SteelColumnDesignEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_column_design(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    c=SteelColumn(f"C{i}","W14X38","ASTM_A992",3.5,ColumnEndCondition.PINNED_PINNED,ColumnEndCondition.PINNED_PINNED,SteelColumnDemand(500e3,30e3,5e3))
    r=SteelColumnDesignEngine().design(c,pr.get("W14X38"),mr.get("ASTM_A992"))
    assert r.unity_ratio>=0
    assert r.compression_capacity>0
