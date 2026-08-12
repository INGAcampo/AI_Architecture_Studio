import pytest
from design.steel.brace_domain import *
from design.steel.brace_design_engine import SteelBraceDesignEngine
from design.steel.brace_optimizer import SteelBraceOptimizer
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_brace_optimizer(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    b=SteelBrace(f"BR{i}","HEA300","ASTM_A992",3,1,BraceBehavior.TENSION_COMPRESSION,BraceConfiguration.X_BRACE,SteelBraceDemand(100e3))
    r=SteelBraceOptimizer(SteelBraceDesignEngine()).optimize(b,pr.get("HEA300"),mr.get("ASTM_A992"),pr.all())
    assert r.recommended_profile_id is not None
