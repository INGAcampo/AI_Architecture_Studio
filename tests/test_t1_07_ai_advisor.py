import pytest
from design.steel.domain import SteelDesignResult
from design.steel.ai_advisor import *
@pytest.mark.parametrize('i',range(120))
def test_ai(i):
 r=SteelDesignResult(f'B{i}',0,0,.9,.9,.9,True,'interaction');a=SteelAIAdvisor();assert 'cumple' in a.explain_design(r).message and a.critical_members((r,),.8)==(r,)
