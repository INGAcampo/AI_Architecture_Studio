import pytest
from engines.structural.platform.members import *
from engines.structural.platform.beams import *
from engines.structural.core.properties import SectionProperties
from engines.structural.core.materials import *

@pytest.mark.parametrize("i",range(120))
def test_beam(i):
    m=StructuralMember(f"B{i}",MemberKind.BEAM,(0,0,3),(6,0,3),"S","MAT")
    b=BeamInstance(m,"BF","BT")
    p=SectionProperties(0.12,0.0016,0.0009,0.002,0.115,0.087,0.008,0.006)
    mat=StructuralMaterial("MAT","Concrete",MaterialCategory.CONCRETE,30e9,12e9,0.2,2400,compressive_strength=30e6)
    e=NativeBimBeamEngine()
    assert e.span(b)==pytest.approx(6)
    assert e.line_weight(b,p,mat)>0
    assert e.validate(b)==()
