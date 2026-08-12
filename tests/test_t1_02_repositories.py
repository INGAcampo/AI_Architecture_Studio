import pytest
from design.steel.domain import *
from design.steel.repositories import *
@pytest.mark.parametrize('i',range(120))
def test_repo(i):
 r=SteelProfileRepository();p=SteelProfile(f'W{i}','W12X26',SteelProfileFamily.W,.0049,38.7,1e-4,2e-5,2e-4,8e-5,2.2e-4,9e-5,.143,.064);r.register(p);assert r.search('W12')==(p,)
