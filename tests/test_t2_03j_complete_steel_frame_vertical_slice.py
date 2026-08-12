import pytest
from types import SimpleNamespace
from design.steel.frame_domain import *
from design.steel.frame_vertical_slice import CompleteSteelFrameVerticalSlice

@pytest.mark.parametrize("i", range(120))
def test_complete_frame(i):
    frame=SteelFrame(f"F{i}")
    frame.add_node(FrameNode("N1",0,0,0)); frame.add_node(FrameNode("N2",5,0,0))
    frame.add_member(FrameMemberRef("B1",FrameMemberType.BEAM,"N1","N2","W14X38","ASTM_A992"))
    beam=SimpleNamespace(member_id="B1",unity_ratio=0.5,passed=True,governing_check="flexure")
    opt=SimpleNamespace(member_id="B1",current_profile_id="W14X38",recommended_profile_id="W12X26",weight_reduction_percent=31.63)
    r=CompleteSteelFrameVerticalSlice().run(frame,"N1",("N2",),(beam,),(),(),opt)
    assert r.connectivity.valid
    assert "# Complete Steel Frame Report" in r.report.markdown
