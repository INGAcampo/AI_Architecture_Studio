"""Finite-value, tolerance, residual and solver-convergence quality controls."""
from __future__ import annotations
import math

class CalculationValidationEngine:
    """Provide reusable numerical acceptance checks for engineering consumers."""
    @staticmethod
    def finite(value):
        """Recursively confirm that scalar or sequence values are numerically finite."""
        if isinstance(value, (list, tuple)):
            return all(CalculationValidationEngine.finite(v) for v in value)
        return math.isfinite(float(value))

    @staticmethod
    def close(actual, expected, tolerance=1e-9):
        """Compare scalar values using an explicit absolute tolerance."""
        return abs(actual - expected) <= tolerance

    @staticmethod
    def residual_linear(a, x, b):
        """Return the Euclidean residual norm of a solved linear system."""
        residuals = [sum(a[i][j]*x[j] for j in range(len(x))) - b[i] for i in range(len(a))]
        return math.sqrt(sum(r*r for r in residuals))

    @staticmethod
    def assert_converged(result):
        """Reject nonconverged solvers or nonfinite residual evidence."""
        if not result.converged:
            raise ValueError("solver_not_converged")
        if not math.isfinite(result.residual):
            raise ValueError("invalid_residual")
        return True
