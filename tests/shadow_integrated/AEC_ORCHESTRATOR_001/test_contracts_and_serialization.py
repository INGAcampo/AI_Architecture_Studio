from aec_orchestrator.contracts import (
    AecApplication,
    JobCommand,
    JobEnvelope,
    WorkerCapability,
)
from aec_orchestrator.serialization import (
    canonical_job_json,
    canonical_job_sha256,
)


def test_capability_support_is_explicit():
    capability = WorkerCapability(
        application=AecApplication.AUTOCAD,
        operations=("probe_runtime", "query_entities"),
    )
    assert capability.supports("probe_runtime") is True
    assert capability.supports("save_drawing") is False


def test_job_serialization_is_deterministic():
    job_a = JobEnvelope(
        job_id="job-1",
        application=AecApplication.AUTOCAD,
        command=JobCommand(
            operation="query_entities",
            payload={"b": 2, "a": 1},
        ),
        idempotency_key="idem-1",
        metadata={"z": 9, "m": 5},
    )
    job_b = JobEnvelope(
        job_id="job-1",
        application=AecApplication.AUTOCAD,
        command=JobCommand(
            operation="query_entities",
            payload={"a": 1, "b": 2},
        ),
        idempotency_key="idem-1",
        metadata={"m": 5, "z": 9},
    )

    assert canonical_job_json(job_a) == canonical_job_json(job_b)
    assert canonical_job_sha256(job_a) == canonical_job_sha256(job_b)


def test_invalid_job_fails_closed():
    failed = False
    try:
        JobEnvelope(
            job_id="",
            application=AecApplication.REVIT,
            command=JobCommand(operation="open_model"),
            idempotency_key="idem",
        ).validate()
    except ValueError:
        failed = True
    assert failed is True
