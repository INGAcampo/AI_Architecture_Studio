import pytest
from platform_sdk.platform import *
@pytest.mark.parametrize("i",range(120))
def test_platform(i):
    sdk=AIASPlatformSDK(); assert not sdk.status().ready
    s=sdk.start(); assert s.ready and s.active_workspace=="analysis" and "platform.context" in s.services
