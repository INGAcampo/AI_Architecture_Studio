import pytest
from platform_sdk.context import PlatformContext
from design.steel.plugin import SteelPlatformPlugin
@pytest.mark.parametrize('i',range(120))
def test_plugin(i):
 c=PlatformContext.create_default();SteelPlatformPlugin().activate(c);assert len(c.services.resolve('steel.profiles').all())==5 and c.workspaces.active.workspace_id=='steel'
