"""Traceable nonlinear-solver result and calculation reference-case contracts."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class SolverResult:
    """Solver value, convergence state, iterations, residual, method and trace."""
    value: Any
    converged: bool
    iterations: int
    residual: float
    method: str
    trace: list[dict[str, Any]] = field(default_factory=list)

@dataclass(slots=True)
class CalculationCase:
    """Expected calculation behavior with tolerance and requirement traceability."""
    case_id: str
    title: str
    inputs: dict[str, Any]
    expected: Any
    tolerance: float
    method: str
    traceability: dict[str, Any]
