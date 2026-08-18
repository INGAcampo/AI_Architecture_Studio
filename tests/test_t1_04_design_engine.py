import pytest
from design.steel.domain import *
from design.steel.design_engine import *
@pytest.mark.parametrize('i',range(120))
def test_design(i):
 p=SteelProfile('W','W',SteelProfileFamily.W,.0072,56.6,2e-4,3e-5,3e-4,9e-5,3.4e-4,1e-4,.17,.07);m=SteelMaterial('M','M',345e6,450e6,200e9,7850);b=SteelBeam(f'B{i}','W','M',6,2,SteelMemberDemand(50e3,30e3,60e3));r=SteelDesignEngine().design(b,p,m);assert r.unity_ratio>=0
