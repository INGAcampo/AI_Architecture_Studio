from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from enum import Enum

from .contracts import JobEnvelope


def _normalize(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    return value


def canonical_job_dict(job: JobEnvelope) -> dict:
    job.validate()
    return _normalize(asdict(job))


def canonical_job_json(job: JobEnvelope) -> str:
    return json.dumps(
        canonical_job_dict(job),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def canonical_job_sha256(job: JobEnvelope) -> str:
    encoded = canonical_job_json(job).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()
