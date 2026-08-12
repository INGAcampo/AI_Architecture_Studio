from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True, slots=True)
class ConstraintCheck:
    constraint_id: str
    passed: bool
    message: str = ""

class ConstraintAdapter:
    def __init__(self):
        self._constraints: list[tuple[str, Callable[[Any], bool], str]] = []

    def register(self, constraint_id: str, predicate: Callable[[Any], bool], message: str = ""):
        if not constraint_id.strip():
            raise ValueError("constraint_id es obligatorio")
        self._constraints.append((constraint_id, predicate, message))

    def check(self, candidate):
        return tuple(
            ConstraintCheck(cid, bool(predicate(candidate)), message)
            for cid, predicate, message in self._constraints
        )

    def is_feasible(self, candidate):
        return all(check.passed for check in self.check(candidate))
