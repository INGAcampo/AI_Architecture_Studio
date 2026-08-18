from aec_orchestrator_reconcile.envelope import ReconciliationExecutionEnvelope,evaluate_execution_envelope


def base(**kwargs):
    values={
        "canonical_head":"abc",
        "expected_canonical_head":"abc",
        "dry_run_passed":True,
        "targeted_tests_passed":True,
        "integration_authorized":True,
        "external_write_authorized":False,
    }
    values.update(kwargs)
    return ReconciliationExecutionEnvelope(**values)


def test_valid_envelope_is_accepted():
    accepted,reason=evaluate_execution_envelope(base())
    assert accepted is True
    assert reason=="accepted"


def test_head_drift_is_blocked():
    accepted,reason=evaluate_execution_envelope(base(canonical_head="new"))
    assert accepted is False
    assert reason=="canonical_head_drift"


def test_missing_integration_authorization_is_blocked():
    accepted,reason=evaluate_execution_envelope(base(integration_authorized=False))
    assert accepted is False
    assert reason=="integration_not_authorized"


def test_external_write_scope_is_blocked():
    accepted,reason=evaluate_execution_envelope(base(external_write_authorized=True))
    assert accepted is False
    assert reason=="external_write_scope_not_permitted_in_reconciliation"
