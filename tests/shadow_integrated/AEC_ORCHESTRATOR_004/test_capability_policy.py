from aec_orchestrator_security.policy import OperationPolicy
from aec_orchestrator_security.capability import CapabilityToken,authorize_operation


POLICY=OperationPolicy(
    application="AUTOCAD",
    allowed_operations=("query","create_transient","save","publish"),
    destructive_operations=("save",),
    publish_operations=("publish",),
)


def test_read_operation_can_be_authorized():
    token=CapabilityToken("AUTOCAD",("query",))
    d=authorize_operation(token,POLICY,"query")
    assert d.authorized is True


def test_save_requires_explicit_destructive_grant():
    token=CapabilityToken("AUTOCAD",("save",),allow_destructive=False)
    d=authorize_operation(token,POLICY,"save")
    assert d.authorized is False
    assert d.reason=="destructive_authorization_required"


def test_publish_requires_explicit_publish_grant():
    token=CapabilityToken("AUTOCAD",("publish",),allow_publish=False)
    d=authorize_operation(token,POLICY,"publish")
    assert d.authorized is False
    assert d.reason=="publish_authorization_required"


def test_cross_application_token_fails_closed():
    token=CapabilityToken("REVIT",("query",))
    d=authorize_operation(token,POLICY,"query")
    assert d.authorized is False
    assert d.reason=="application_mismatch"
