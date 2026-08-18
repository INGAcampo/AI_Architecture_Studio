import pytest
from design.steel.domain import *
from design.steel.design_engine import SteelDesignEngine
from design.steel.optimizer import *
@pytest.mark.parametrize('i',range(120))
def test_opt(i):
 p=SteelProfile('P','P',SteelProfileFamily.W,.01,50,1,1,1,1,1,1,1,1);m=SteelMaterial('M','M',345e6,450e6,200e9,7850);b=SteelBeam(f'B{i}','P','M',5,2,SteelMemberDemand(moment=1));r=SteelProfileOptimizer(SteelDesignEngine()).optimize(b,p,m,(p,));assert r.recommended_profile_id=='P'
