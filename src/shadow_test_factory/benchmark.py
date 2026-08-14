from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkResult:
    label: str
    iterations: int
    elapsed_seconds: float
    operations_per_second: float


def benchmark(label: str, operation, *, iterations: int = 10000) -> BenchmarkResult:
    if not label.strip():
        raise ValueError("label must not be empty")
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    start = time.perf_counter()
    for _ in range(iterations):
        operation()
    elapsed = time.perf_counter() - start

    rate = float("inf") if elapsed == 0 else iterations / elapsed

    return BenchmarkResult(
        label=label,
        iterations=iterations,
        elapsed_seconds=elapsed,
        operations_per_second=rate,
    )
