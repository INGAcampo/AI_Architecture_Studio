import pytest
from design.steel.brace_domain import *
from design.steel.brace_design_engine import SteelBraceDesignEngine
from design.steel.brace_batch import BraceBatchDesignEngine
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository

@pytest.mark.parametrize("i", range(120))
def test_batch(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    braces=tuple(SteelBrace(f"BR{i}-{j}","HSS200X200X8","ASTM_A992",4,1,BraceBehavior.TENSION_COMPRESSION,BraceConfiguration.X_BRACE,SteelBraceDemand(100e3)) for j in range(3))
    r=BraceBatchDesignEngine(SteelBraceDesignEngine()).design(braces,pr,mr)
    assert len(r.results)==3
