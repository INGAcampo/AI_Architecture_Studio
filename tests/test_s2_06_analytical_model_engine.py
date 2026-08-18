import pytest
from engines.structural.platform.members import *
from engines.structural.platform.analytical import *
from engines.structural.core.coordinates import StructuralCoordinateSystem

@pytest.mark.parametrize("i",range(120))
def test_analytical(i):
    m=StructuralMember(f"M{i}",MemberKind.BEAM,(0,0,0),(3,4,0),"S","MAT")
    e=AnalyticalModelEngine()
    a=e.build_member(m,"N1","N2",StructuralCoordinateSystem())
    assert a.length==pytest.approx(5)
    assert a.local_axes.x[0]==pytest.approx(0.6)
