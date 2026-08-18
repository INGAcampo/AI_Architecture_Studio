import pytest
from design.steel.brace_tension import BraceTensionEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_tension(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    r=BraceTensionEngine().calculate(pr.get("HSS200X200X8"),mr.get("ASTM_A992"))
    assert r.design_capacity>0
    assert r.governing_mode in {"gross_section_yielding","net_section_rupture"}
