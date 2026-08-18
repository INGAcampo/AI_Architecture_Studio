import pytest
from platform_sdk.bootstrap import *
@pytest.mark.parametrize("i",range(120))
def test_bootstrap(i):
    r=PlatformBootstrap().build()
    assert r.context.services.contains("platform.context")
    assert r.context.workspaces.active.workspace_id=="analysis"
