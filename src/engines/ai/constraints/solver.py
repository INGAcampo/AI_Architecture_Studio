from __future__ import annotations
from dataclasses import dataclass

from .constraint import ConstraintStatus, ConstraintViolation
from .model import ConstraintSystem


@dataclass(frozen=True, slots=True)
class SolverOptions:
    max_iterations: int = 100
    convergence_tolerance: float = 1e-6

    def __post_init__(self) -> None:
        if self.max_iterations < 1:
            raise ValueError("max_iterations inválido")
        if self.convergence_tolerance <= 0:
            raise ValueError("convergence_tolerance inválida")


@dataclass(frozen=True, slots=True)
class SolverResult:
    converged: bool
    iterations: int
    values: dict[str, float]
    violations: tuple[ConstraintViolation, ...]

    @property
    def success(self) -> bool:
        return self.converged and not self.violations


class ConstraintSolver:
    def solve(
        self,
        system: ConstraintSystem,
        *,
        options: SolverOptions | None = None,
    ) -> SolverResult:
        opts = options or SolverOptions()
        values = system.values()
        iterations = 0

        for iteration in range(1, opts.max_iterations + 1):
            iterations = iteration
            max_residual = 0.0
            changed = False

            for constraint in system.constraints():
                if not constraint.enabled:
                    continue
                residual = abs(constraint.residual(values))
                max_residual = max(max_residual, residual)
                changed = constraint.project(values) or changed

            if max_residual <= opts.convergence_tolerance:
                break
            if not changed:
                break

        system.update_values(values)
        final_values = system.values()
        violations = tuple(
            violation
            for constraint in system.constraints()
            if (violation := constraint.violation(final_values)) is not None
        )
        converged = not violations

        return SolverResult(
            converged=converged,
            iterations=iterations,
            values=final_values,
            violations=violations,
        )

    def validate(self, system: ConstraintSystem) -> tuple[ConstraintViolation, ...]:
        values = system.values()
        return tuple(
            violation
            for constraint in system.constraints()
            if (violation := constraint.violation(values)) is not None
        )
