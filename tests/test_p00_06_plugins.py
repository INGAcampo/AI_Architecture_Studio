import pytest
from types import SimpleNamespace
from platform_sdk.plugins import *
from platform_sdk.services import ServiceRegistry
class P:
    manifest=PluginManifest("p","P","1.0",("analysis",))
    def activate(self,c): c.state.append("ok")
@pytest.mark.parametrize("i",range(120))
def test_plugins(i):
    s=ServiceRegistry(); s.register("analysis",object()); c=SimpleNamespace(services=s,state=[])
    m=PluginManager(); m.register(P()); m.activate("p",c)
    assert m.is_active("p") and c.state==["ok"]
