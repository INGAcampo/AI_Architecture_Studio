import pytest
from design.steel.brace_compression import BraceCompressionEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_compression(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    r=BraceCompressionEngine().calculate(pr.get("HSS200X200X8"),mr.get("ASTM_A992"),70)
    assert r.design_capacity>0
