import pytest
from platform_sdk.services import *
@pytest.mark.parametrize("i",range(120))
def test_service(i):
    r=ServiceRegistry(); o={"i":i}; r.register("analysis",o)
    assert r.resolve("analysis") is o and r.ids()==("analysis",)
