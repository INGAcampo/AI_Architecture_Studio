from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

@dataclass(frozen=True, slots=True)
class ScheduledResult:
    index: int
    value: object
    error: str | None = None

class AsyncExecutionScheduler:
    def __init__(self, max_workers: int = 4):
        if max_workers < 1:
            raise ValueError("max_workers inválido")
        self.max_workers = max_workers

    def map(self, function, items):
        items = tuple(items)
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(function, item) for item in items]
            for index, future in enumerate(futures):
                try:
                    results.append(ScheduledResult(index, future.result()))
                except Exception as exc:
                    results.append(ScheduledResult(index, None, str(exc)))
        return tuple(results)
