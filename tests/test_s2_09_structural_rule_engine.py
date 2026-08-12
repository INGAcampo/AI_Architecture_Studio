import pytest
from engines.structural.platform.members import *
from engines.structural.platform.rules import *
from engines.structural.core.properties import SectionProperties
from engines.structural.core.materials import *

@pytest.mark.parametrize("i",range(120))
def test_rules(i):
    m=StructuralMember(f"M{i}",MemberKind.COLUMN,(0,0,0),(0,0,5),"S","MAT")
    p=SectionProperties(0.01,1e-6,1e-6,1,0.01,0.01,1,1)
    mat=StructuralMaterial("MAT","Steel",MaterialCategory.STEEL,200e9,77e9,0.3,7850,yield_strength=355e6)
    issues=StructuralRuleEngine().review_member(m,p,mat)
    assert issues[0].rule_id=="member.slenderness"
