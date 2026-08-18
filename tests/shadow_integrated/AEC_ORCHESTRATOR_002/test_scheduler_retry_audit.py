from aec_orchestrator_ext.scheduler import JobDependency, build_dispatch_plan
from aec_orchestrator_ext.retry import RetryPolicy, evaluate_retry
from aec_orchestrator_ext.audit import AuditTrail


def test_scheduler_builds_parallel_waves():
    plan = build_dispatch_plan(
        (
            JobDependency("A"),
            JobDependency("B"),
            JobDependency("C", ("A", "B")),
            JobDependency("D", ("C",)),
        )
    )
    assert plan.waves == (("A", "B"), ("C",), ("D",))


def test_scheduler_rejects_cycles():
    failed = False
    try:
        build_dispatch_plan(
            (
                JobDependency("A", ("B",)),
                JobDependency("B", ("A",)),
            )
        )
    except ValueError as exc:
        failed = "cycle" in str(exc)
    assert failed is True


def test_retry_policy_is_explicit_and_bounded():
    policy = RetryPolicy(max_attempts=3)
    d1 = evaluate_retry(current_attempt=1, error_code="timeout", policy=policy)
    d2 = evaluate_retry(current_attempt=3, error_code="timeout", policy=policy)

    assert d1.should_retry is True
    assert d1.next_attempt == 2
    assert d2.should_retry is False


def test_nonretryable_error_fails_closed():
    policy = RetryPolicy()
    decision = evaluate_retry(
        current_attempt=1,
        error_code="authorization_denied",
        policy=policy,
    )
    assert decision.should_retry is False
    assert decision.reason == "error_is_not_retryable"


def test_audit_trail_is_monotonic():
    trail = AuditTrail()
    a = trail.append("job-1", "CREATED")
    b = trail.append("job-1", "DISPATCHED")
    c = trail.append("job-1", "SUCCEEDED")

    assert (a.sequence, b.sequence, c.sequence) == (1, 2, 3)
    assert tuple(e.event_type for e in trail.events) == (
        "CREATED",
        "DISPATCHED",
        "SUCCEEDED",
    )
