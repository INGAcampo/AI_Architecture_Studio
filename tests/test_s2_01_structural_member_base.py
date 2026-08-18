import pytest
from engines.structural.platform.members import *

@pytest.mark.parametrize("i",range(120))
def test_member(i):
    m=StructuralMember(f"M{i}",MemberKind.BEAM,(0,0,0),(3,4,0),"S1","MAT")
    assert m.length==pytest.approx(5)
    m2=m.with_end((6,8,0))
    assert m2.length==pytest.approx(10) and m2.revision==1
