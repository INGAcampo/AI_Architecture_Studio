import pytest
from design.steel.domain import *
from design.steel.reports import *
@pytest.mark.parametrize('i',range(120))
def test_report(i):
 p=SteelProfile('P','P',SteelProfileFamily.W,.01,50,1,1,1,1,1,1,1,1);m=SteelMaterial('M','M',1,1,1,1);b=SteelBeam(f'B{i}','P','M',1,1);r=SteelDesignResult(b.member_id,0,0,0,0,0,True,'axial');assert 'PASS' in SteelReportEngine().build(b,p,m,r).markdown
