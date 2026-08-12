import pytest
from engines.structural.platform.members import *
from engines.structural.platform.columns import *
from engines.structural.core.properties import SectionProperties
from engines.structural.core.materials import *

@pytest.mark.parametrize("i",range(120))
def test_column(i):
    m=StructuralMember(f"C{i}",MemberKind.COLUMN,(0,0,0),(0,0,3),"S","MAT")
    c=ColumnInstance(m,ColumnConstraints("L1","L2"),"CF","CT")
    p=SectionProperties(0.09,0.000675,0.000675,0.001,0.0866,0.0866,0.0045,0.0045)
    mat=StructuralMaterial("MAT","Concrete",MaterialCategory.CONCRETE,30e9,12e9,0.2,2400,compressive_strength=30e6)
    e=NativeBimColumnEngine()
    assert e.axial_length(c)==pytest.approx(3)
    assert e.self_weight(c,p,mat)>0
    assert e.validate(c,p)==()
