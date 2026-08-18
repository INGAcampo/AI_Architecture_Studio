import pytest
from platform_sdk.commands import *
@pytest.mark.parametrize("i",range(120))
def test_commands(i):
    b=CommandBus(); b.register_handler("double",lambda x:x*2)
    r=b.execute(PlatformCommand("double",i))
    assert r.completed and r.value==i*2
