import pytest
from types import SimpleNamespace
from design.steel.frame_reports import SteelFrameReportEngine
from design.steel.frame_domain import SteelFrame

@pytest.mark.parametrize("i", range(120))
def test_frame_report(i):
    frame=SteelFrame(f"F{i}")
    dashboard=SimpleNamespace(total_members=3,passed_members=3,failed_members=0,maximum_unity=0.8,critical_members=())
    opt=SimpleNamespace(optimized_members=2,average_weight_reduction_percent=12.5)
    advice=SimpleNamespace(summary="OK",warnings=(),recommendations=("Optimizar",))
    r=SteelFrameReportEngine().build(frame,dashboard,opt,advice)
    assert f"Complete Steel Frame Report — F{i}" in r.markdown
