from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class FuzzSummary:
    seed: int
    iterations: int
    failures: int


def run_numeric_invariant_fuzz(
    invariant,
    *,
    seed: int = 1,
    iterations: int = 1000,
    low: float = -1000.0,
    high: float = 1000.0,
) -> FuzzSummary:
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    rng = random.Random(seed)
    failures = 0

    for _ in range(iterations):
        value = rng.uniform(low, high)
        try:
            ok = bool(invariant(value))
        except Exception:
            ok = False
        if not ok:
            failures += 1

    return FuzzSummary(
        seed=seed,
        iterations=iterations,
        failures=failures,
    )
