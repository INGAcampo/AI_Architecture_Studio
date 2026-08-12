import pytest
from platform_sdk.context import PlatformContext
from design.steel.workspace import SteelWorkspace
@pytest.mark.parametrize('i',range(120))
def test_workspace(i):
 c=PlatformContext.create_default();w=SteelWorkspace().install(c);assert c.workspaces.active.workspace_id=='steel' and c.services.resolve('workspace.steel') is w
