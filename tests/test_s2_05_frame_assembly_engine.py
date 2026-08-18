import pytest
from engines.structural.core.graph import *
from engines.structural.platform.frames import *

@pytest.mark.parametrize("i",range(120))
def test_frames(i):
    g=StructuralGraph()
    m1=StructuralMember("M1","N1","N2","S","MAT","column")
    m2=StructuralMember("M2","N2","N3","S","MAT","beam")
    g.add_member(m1);g.add_member(m2)
    e=FrameAssemblyEngine();f=e.assemble(f"F{i}",(m1,m2))
    assert f.member_ids==("M1","M2")
    assert e.is_connected(f,g)
