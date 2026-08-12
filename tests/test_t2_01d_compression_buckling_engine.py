import pytest
from design.steel.compression_buckling import CompressionBucklingEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_buckling(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    r=CompressionBucklingEngine().calculate(pr.get("W14X38"),mr.get("ASTM_A992"),80)
    assert r.design_capacity>0
    assert r.critical_stress>0
