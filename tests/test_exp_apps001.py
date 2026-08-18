from dataclasses import replace

import pytest

from aias_application_platform import ApplicationManifest, ApplicationRegistry, ContractBroker, ProjectEnvelope, SyncRequest


def app(*, zone="LOCAL_TRUSTED", scopes=("project:read", "project:propose"), offline=True):
    registry = ApplicationRegistry()
    manifest = ApplicationManifest("AIAS-APP-DESKTOP", "AIAS Desktop", "DESKTOP", zone, scopes=scopes, offline_supported=offline)
    registry.register(manifest)
    registry.transition(manifest.app_id, "APPROVED", {"approval": "AEC-000052"})
    registry.transition(manifest.app_id, "VALIDATED", {"validation": "tests/test_exp_apps001.py"})
    return registry


def project(sensitivity="INTERNAL", revision=4):
    return ProjectEnvelope("AIAS-PRJ-A1B2C3D4", "VE", sensitivity, revision, "aias://projects/AIAS-PRJ-A1B2C3D4", capability_refs=("WORKSPACE-2",))


def test_project_envelope_is_deterministic_and_secret_safe():
    assert project().fingerprint() == project().fingerprint()
    with pytest.raises(ValueError, match="secret_material_forbidden"):
        replace(project(), metadata={"token": "never-store-this"}).validate()


def test_application_cannot_claim_source_of_truth():
    with pytest.raises(ValueError, match="applications_cannot_own"):
        replace(app().get("AIAS-APP-DESKTOP"), source_of_truth=True).validate()


def test_registry_requires_sequential_evidence_gates():
    registry = ApplicationRegistry()
    manifest = ApplicationManifest("AIAS-APP-WEB", "AIAS Web", "WEB", "PUBLIC_EDGE")
    registry.register(manifest)
    with pytest.raises(ValueError, match="invalid_lifecycle_transition"):
        registry.transition(manifest.app_id, "VALIDATED", {"validation": "x"})
    with pytest.raises(ValueError, match="missing_gate_evidence"):
        registry.transition(manifest.app_id, "APPROVED", {})


def test_broker_allows_scoped_valid_projection():
    broker = ContractBroker(app())
    decision = broker.authorize(SyncRequest("AIAS-APP-DESKTOP", project(), "project.propose", 4))
    assert decision.allowed and len(decision.evidence["fingerprint"]) == 64


def test_stale_mutation_is_denied():
    decision = ContractBroker(app()).authorize(SyncRequest("AIAS-APP-DESKTOP", project(), "project.propose", 3))
    assert not decision.allowed and decision.reason == "stale_revision"


def test_public_edge_cannot_access_regulated_project():
    decision = ContractBroker(app(zone="PUBLIC_EDGE")).authorize(SyncRequest("AIAS-APP-DESKTOP", project("REGULATED"), "project.read", 4))
    assert not decision.allowed and decision.reason == "regulated_project_public_edge_denied"


def test_scope_and_offline_behavior_fail_closed():
    broker = ContractBroker(app(scopes=("project:read",), offline=False))
    assert broker.authorize(SyncRequest("AIAS-APP-DESKTOP", project(), "project.propose", 4)).reason == "scope_denied"
    assert broker.authorize(SyncRequest("AIAS-APP-DESKTOP", project(), "project.read", 4, offline=True)).reason == "offline_not_supported"
