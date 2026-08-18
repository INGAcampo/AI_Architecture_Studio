from dataclasses import dataclass
from copy import deepcopy

@dataclass(frozen=True, slots=True)
class TransactionOutcome:
    committed: bool
    error: str | None = None

class KernelTransaction:
    def __init__(self, target):
        self.target = target
        self._snapshot = deepcopy(target.__dict__)

    def commit(self, operation):
        try:
            operation()
            return TransactionOutcome(True)
        except Exception as exc:
            self.target.__dict__.clear()
            self.target.__dict__.update(deepcopy(self._snapshot))
            return TransactionOutcome(False, str(exc))
