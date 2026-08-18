import pytest
from engines.structural.platform.members import *
from engines.structural.platform.visualization import *

@pytest.mark.parametrize("i",range(120))
def test_visualization(i):
    m=StructuralMember(f"M{i}",MemberKind.COLUMN,(0,0,0),(0,0,3),"S1","MAT")
    e=StructuralVisualizationEngine();v=e.member_visual(m,0.85)
    assert v.label=="column:S1"
    assert e.filter_by_utilization((v,),0.8)==(v,)
