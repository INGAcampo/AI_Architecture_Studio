import pytest
from design.steel.repositories import *
from design.steel.catalog import *
@pytest.mark.parametrize('i',range(120))
def test_catalog(i):
 pr=SteelProfileRepository();mr=SteelMaterialRepository();ps,ms=seed_default_catalog(pr,mr);assert len(ps)==5 and mr.get('ASTM_A992').fy==pytest.approx(345e6)
