import pytest
from platform_sdk.workspaces import *
@pytest.mark.parametrize("i",range(120))
def test_workspaces(i):
    m=WorkspaceManager(); m.register(WorkspaceDefinition("architecture","Architecture"))
    m.register(WorkspaceDefinition("analysis","Analysis",("loads","results")))
    assert m.activate("analysis").panels==("loads","results")
