import pytest
from design.steel.brace_domain import *
from design.steel.brace_design_engine import SteelBraceDesignEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_brace_design(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    b=SteelBrace(f"BR{i}","HSS200X200X8","ASTM_A992",4,1,BraceBehavior.TENSION_COMPRESSION,BraceConfiguration.X_BRACE,SteelBraceDemand(-250e3))
    r=SteelBraceDesignEngine().design(b,pr.get("HSS200X200X8"),mr.get("ASTM_A992"))
    assert r.unity_ratio>=0
    assert r.compression_capacity>0
