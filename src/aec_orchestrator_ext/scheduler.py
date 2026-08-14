from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobDependency:
    job_id: str
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class DispatchPlan:
    waves: tuple[tuple[str, ...], ...]


def build_dispatch_plan(dependencies: tuple[JobDependency, ...]) -> DispatchPlan:
    if not dependencies:
        return DispatchPlan(waves=())

    graph = {}
    for item in dependencies:
        if not item.job_id.strip():
            raise ValueError("job_id must not be empty")
        if item.job_id in graph:
            raise ValueError("duplicate job_id")
        graph[item.job_id] = set(item.depends_on)

    known = set(graph)
    for job_id, deps in graph.items():
        unknown = deps - known
        if unknown:
            raise KeyError(f"{job_id} depends on unknown jobs: {sorted(unknown)}")

    remaining = {key: set(value) for key, value in graph.items()}
    completed = set()
    waves = []

    while remaining:
        ready = sorted(
            job_id
            for job_id, deps in remaining.items()
            if deps.issubset(completed)
        )

        if not ready:
            raise ValueError("dependency cycle detected")

        waves.append(tuple(ready))
        for job_id in ready:
            completed.add(job_id)
            del remaining[job_id]

    return DispatchPlan(waves=tuple(waves))
