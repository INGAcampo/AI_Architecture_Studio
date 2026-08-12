import pytest
from design.steel.column_domain import *
from design.steel.column_design_engine import SteelColumnDesignEngine
from design.steel.column_optimizer import SteelColumnOptimizer
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_column_optimizer(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    c=SteelColumn(f"C{i}","HEA300","ASTM_A992",3.0,ColumnEndCondition.FIXED_FIXED,ColumnEndCondition.FIXED_FIXED,SteelColumnDemand(200e3,10e3,5e3))
    r=SteelColumnOptimizer(SteelColumnDesignEngine()).optimize(c,pr.get("HEA300"),mr.get("ASTM_A992"),pr.all())
    assert r.recommended_profile_id is not None
