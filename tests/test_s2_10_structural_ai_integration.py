import pytest
from engines.structural.platform.members import *
from engines.structural.platform.ai_integration import *

@pytest.mark.parametrize("i",range(120))
def test_ai_integration(i):
    m=StructuralMember(f"M{i}",MemberKind.BEAM,(0,0,0),(5,0,0),"S","MAT")
    d=StructuralAIIntegration().recommend_section(m,120,(("S1",100),("S2",130),("S3",160)))
    assert d.recommended_section_id=="S2"
    assert d.confidence>0
