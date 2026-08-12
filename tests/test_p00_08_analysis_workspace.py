import pytest
from platform_sdk.context import PlatformContext
from platform_sdk.analysis_workspace import AnalysisWorkspace
@pytest.mark.parametrize("i",range(120))
def test_analysis_workspace(i):
    c=PlatformContext.create_default(); w=AnalysisWorkspace().install(c)
    assert c.workspaces.active.workspace_id=="analysis"
    assert c.services.resolve("workspace.analysis") is w
