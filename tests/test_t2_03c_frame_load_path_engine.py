import pytest
from design.steel.frame_domain import *
from design.steel.frame_load_path import FrameLoadPathEngine

@pytest.mark.parametrize("i", range(120))
def test_load_path(i):
    f=SteelFrame(f"F{i}")
    for nid,x in (("N1",0),("N2",1),("N3",2)): f.add_node(FrameNode(nid,x,0,0))
    f.add_member(FrameMemberRef("M1",FrameMemberType.BEAM,"N1","N2","W14X38","ASTM_A992"))
    f.add_member(FrameMemberRef("M2",FrameMemberType.COLUMN,"N2","N3","W14X38","ASTM_A992"))
    r=FrameLoadPathEngine().trace(f,"N1",("N3",))
    assert r.path_exists and r.support_nodes==("N3",)
