import pytest
from design.steel.frame_domain import *

@pytest.mark.parametrize("i", range(120))
def test_frame_domain(i):
    f=SteelFrame(f"F{i}")
    f.add_node(FrameNode("N1",0,0,0)); f.add_node(FrameNode("N2",5,0,0))
    m=f.add_member(FrameMemberRef("B1",FrameMemberType.BEAM,"N1","N2","W14X38","ASTM_A992"))
    assert f.members_by_type(FrameMemberType.BEAM)==(m,)
