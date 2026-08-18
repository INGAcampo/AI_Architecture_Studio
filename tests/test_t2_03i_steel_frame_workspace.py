import pytest
from platform_sdk.context import PlatformContext
from design.steel.frame_workspace import SteelFrameWorkspace

@pytest.mark.parametrize("i", range(120))
def test_frame_workspace(i):
    c=PlatformContext.create_default()
    w=SteelFrameWorkspace().install(c)
    assert c.workspaces.active.workspace_id=="steel_frame"
    assert "critical_dashboard" in w.definition().panels
