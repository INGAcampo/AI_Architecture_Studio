import pytest
from design.steel.brace_domain import *
from design.steel.brace_slenderness import BraceSlendernessEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_brace_slenderness(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    b=SteelBrace(f"BR{i}","HSS200X200X8","ASTM_A992",4,1,BraceBehavior.TENSION_COMPRESSION,BraceConfiguration.X_BRACE,SteelBraceDemand(100e3))
    r=BraceSlendernessEngine().calculate(b,pr.get("HSS200X200X8"))
    assert r.slenderness>0
