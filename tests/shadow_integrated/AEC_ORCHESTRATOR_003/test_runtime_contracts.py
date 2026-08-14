from aec_orchestrator_runtime.lease import WorkerLease,evaluate_lease
from aec_orchestrator_runtime.budget import TimeoutBudget,consume_budget
from aec_orchestrator_runtime.cancel import CancellationToken


def test_worker_lease_is_valid_before_expiry():
    lease=WorkerLease("worker-1",100.0,30.0)
    d=evaluate_lease(lease,120.0)
    assert d.valid is True
    assert d.remaining_s==10.0


def test_worker_lease_expires_fail_closed():
    lease=WorkerLease("worker-1",100.0,30.0)
    d=evaluate_lease(lease,130.0)
    assert d.valid is False
    assert d.reason=="lease_expired"


def test_timeout_budget_never_goes_negative():
    b=TimeoutBudget(10.0)
    b=consume_budget(b,7.0)
    b=consume_budget(b,8.0)
    assert b.consumed_s==10.0
    assert b.remaining_s==0.0


def test_cancellation_is_idempotent():
    token=CancellationToken()
    token.cancel("user_request")
    token.cancel("second_reason")
    assert token.cancelled is True
    assert token.reason=="user_request"
