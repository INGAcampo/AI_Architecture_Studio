"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from dataclasses import dataclass, field
from time import perf_counter

@dataclass(slots=True)
class Observability:
    """Execute the public Observability operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    events: list[dict] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)

    def emit(self, name: str, **payload) -> None:
        """Execute the public Observability.emit operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        self.events.append({"name": name, **payload})

    def time_call(self, metric: str, fn, *args, **kwargs):
        """Execute the public Observability.time_call operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        start = perf_counter()
        result = fn(*args, **kwargs)
        self.metrics[metric] = perf_counter() - start
        return result
