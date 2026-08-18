import pytest
from platform_sdk.context import *
@pytest.mark.parametrize("i",range(120))
def test_context(i):
    c=PlatformContext.create_default(); c.services.register("value",i)
    assert c.services.resolve("value")==i and c.documents.active is None
