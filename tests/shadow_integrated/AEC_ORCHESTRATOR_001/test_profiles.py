from aec_orchestrator.contracts import AecApplication
from aec_orchestrator.profiles import DEFAULT_CAPABILITIES


def test_all_declared_aec_applications_have_default_capabilities():
    assert set(DEFAULT_CAPABILITIES) == set(AecApplication)


def test_default_profiles_are_probeable():
    for application, capability in DEFAULT_CAPABILITIES.items():
        assert capability.application == application
        assert capability.supports("probe_runtime")
        assert capability.protocol_version == "1.0"
