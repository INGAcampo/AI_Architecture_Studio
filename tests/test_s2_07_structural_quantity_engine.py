import pytest
from engines.structural.platform.members import *
from engines.structural.platform.quantities import *
from engines.structural.core.properties import SectionProperties
from engines.structural.core.materials import *

@pytest.mark.parametrize("i",range(120))
def test_quantities(i):
    m=StructuralMember(f"M{i}",MemberKind.BEAM,(0,0,0),(5,0,0),"S","MAT")
    p=SectionProperties(0.1,1,1,1,1,1,1,1)
    mat=StructuralMaterial("MAT","Steel",MaterialCategory.STEEL,200e9,77e9,0.3,7850,yield_strength=355e6)
    q=StructuralQuantityEngine().calculate(m,p,mat)
    assert q.volume==pytest.approx(0.5)
    assert q.mass==pytest.approx(3925)
