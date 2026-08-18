import pytest
from design.steel.frame_domain import *
from design.steel.frame_connectivity import FrameConnectivityEngine

@pytest.mark.parametrize("i", range(120))
def test_connectivity(i):
    f=SteelFrame(f"F{i}")
    f.add_node(FrameNode("N1",0,0,0)); f.add_node(FrameNode("N2",5,0,0))
    f.add_member(FrameMemberRef("B1",FrameMemberType.BEAM,"N1","N2","W14X38","ASTM_A992"))
    r=FrameConnectivityEngine().analyze(f)
    assert r.valid
    assert r.node_members["N1"]==["B1"]
