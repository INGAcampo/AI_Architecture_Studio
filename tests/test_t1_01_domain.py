import pytest
from design.steel.domain import *
@pytest.mark.parametrize('i',range(120))
def test_domain(i):
 p=SteelProfile(f'W{i}','W12X26',SteelProfileFamily.W,.0049,38.7,1e-4,2e-5,2e-4,8e-5,2.2e-4,9e-5,.143,.064);m=SteelMaterial('A992','A992',345e6,450e6,200e9,7850);b=SteelBeam(f'B{i}',p.profile_id,m.material_id,6,3,SteelMemberDemand(moment=80e3));assert b.length==6 and p.family is SteelProfileFamily.W
