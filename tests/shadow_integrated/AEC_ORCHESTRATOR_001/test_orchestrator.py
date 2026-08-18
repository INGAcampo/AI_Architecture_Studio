from aec_orchestrator.contracts import (
    AecApplication,
    JobCommand,
    JobEnvelope,
    JobState,
    WorkerCapability,
)
from aec_orchestrator.orchestrator import AecOrchestrator
from aec_orchestrator.worker import DeterministicWorker


def make_worker(application):
    capability = WorkerCapability(
        application=application,
        operations=("echo", "sum_values"),
    )
    worker = DeterministicWorker(capability)
    worker.register("echo", lambda payload: payload)
    worker.register(
        "sum_values",
        lambda payload: {"sum": sum(payload["values"])},
    )
    return worker


def test_dispatch_succeeds_for_registered_worker():
    orchestrator = AecOrchestrator()
    orchestrator.register_worker(make_worker(AecApplication.AUTOCAD))

    job = JobEnvelope(
        job_id="job-1",
        application=AecApplication.AUTOCAD,
        command=JobCommand("sum_values", {"values": [1, 2, 3]}),
        idempotency_key="idem-1",
    )

    result = orchestrator.dispatch(job)

    assert result.state == JobState.SUCCEEDED
    assert result.output["sum"] == 6
    assert len(orchestrator.records) == 1


def test_idempotency_returns_same_completed_result():
    orchestrator = AecOrchestrator()
    orchestrator.register_worker(make_worker(AecApplication.REVIT))

    job = JobEnvelope(
        job_id="job-2",
        application=AecApplication.REVIT,
        command=JobCommand("echo", {"value": 10}),
        idempotency_key="same-key",
    )

    first = orchestrator.dispatch(job)
    second = orchestrator.dispatch(job)

    assert first == second
    assert first.state == JobState.SUCCEEDED


def test_missing_worker_fails_closed():
    orchestrator = AecOrchestrator()

    job = JobEnvelope(
        job_id="job-3",
        application=AecApplication.ETABS,
        command=JobCommand("run_analysis"),
        idempotency_key="idem-3",
    )

    result = orchestrator.dispatch(job)

    assert result.state == JobState.FAILED
    assert "no worker registered" in result.error


def test_undeclared_operation_fails_closed():
    orchestrator = AecOrchestrator()
    orchestrator.register_worker(make_worker(AecApplication.SAP2000))

    job = JobEnvelope(
        job_id="job-4",
        application=AecApplication.SAP2000,
        command=JobCommand("delete_everything"),
        idempotency_key="idem-4",
    )

    result = orchestrator.dispatch(job)

    assert result.state == JobState.FAILED
    assert "not declared" in result.error


def test_cross_application_dispatch_isolated():
    autocad = make_worker(AecApplication.AUTOCAD)
    revit = make_worker(AecApplication.REVIT)

    orchestrator = AecOrchestrator()
    orchestrator.register_worker(autocad)
    orchestrator.register_worker(revit)

    cad_job = JobEnvelope(
        job_id="cad",
        application=AecApplication.AUTOCAD,
        command=JobCommand("echo", {"target": "cad"}),
        idempotency_key="cad-key",
    )
    revit_job = JobEnvelope(
        job_id="revit",
        application=AecApplication.REVIT,
        command=JobCommand("echo", {"target": "revit"}),
        idempotency_key="revit-key",
    )

    assert orchestrator.dispatch(cad_job).output["target"] == "cad"
    assert orchestrator.dispatch(revit_job).output["target"] == "revit"
