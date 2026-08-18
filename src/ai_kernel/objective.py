from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any

class ObjectiveDirection(str, Enum):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"

@dataclass(frozen=True, slots=True)
class ObjectiveResult:
    objective_id: str
    raw_value: float
    normalized_score: float
    direction: ObjectiveDirection

class Objective:
    def __init__(self, objective_id: str, evaluator: Callable[[Any], float], *,
                 direction: ObjectiveDirection = ObjectiveDirection.MINIMIZE,
                 weight: float = 1.0):
        if not objective_id.strip():
            raise ValueError("objective_id es obligatorio")
        if weight <= 0:
            raise ValueError("weight debe ser positivo")
        self.objective_id = objective_id
        self.evaluator = evaluator
        self.direction = direction
        self.weight = float(weight)

    def evaluate(self, candidate):
        value = float(self.evaluator(candidate))
        score = -value if self.direction is ObjectiveDirection.MINIMIZE else value
        return ObjectiveResult(
            self.objective_id,
            value,
            score * self.weight,
            self.direction,
        )
