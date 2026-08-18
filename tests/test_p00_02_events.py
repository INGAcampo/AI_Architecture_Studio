import pytest
from platform_sdk.events import *
@pytest.mark.parametrize("i",range(120))
def test_events(i):
    b=GlobalEventBus(); out=[]; b.subscribe("changed",out.append)
    b.publish(PlatformEvent("changed",i,"cad"))
    assert out[0].payload==i and out[0].source=="cad"
