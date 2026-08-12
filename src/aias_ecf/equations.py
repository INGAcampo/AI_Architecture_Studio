"""Trace-producing scalar nonlinear equation solvers."""
from __future__ import annotations
from .models import SolverResult

class EquationEngine:
    """Solve roots by bisection, Newton and secant methods with convergence evidence."""
    @staticmethod
    def bisection(f, a, b, tolerance=1e-10, max_iter=200):
        """Solve a bracketed scalar root while retaining every residual iteration."""
        fa, fb = f(a), f(b)
        if fa == 0: return SolverResult(a, True, 0, 0.0, "bisection", [])
        if fb == 0: return SolverResult(b, True, 0, 0.0, "bisection", [])
        if fa * fb > 0:
            raise ValueError("root_not_bracketed")
        trace = []
        c = a
        for i in range(1, max_iter + 1):
            c = (a + b) / 2.0
            fc = f(c)
            trace.append({"iteration": i, "x": c, "residual": abs(fc)})
            if abs(fc) <= tolerance or abs(b - a) / 2.0 <= tolerance:
                return SolverResult(c, True, i, abs(fc), "bisection", trace)
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
        return SolverResult(c, False, max_iter, abs(f(c)), "bisection", trace)

    @staticmethod
    def newton(f, df, x0, tolerance=1e-10, max_iter=100):
        """Solve a scalar root from a derivative and reject near-zero slopes."""
        x = float(x0)
        trace = []
        for i in range(1, max_iter + 1):
            fx, dfx = f(x), df(x)
            if abs(dfx) < 1e-15:
                raise ValueError("zero_derivative")
            x_new = x - fx / dfx
            residual = abs(f(x_new))
            trace.append({"iteration": i, "x": x_new, "residual": residual})
            if residual <= tolerance or abs(x_new - x) <= tolerance:
                return SolverResult(x_new, True, i, residual, "newton", trace)
            x = x_new
        return SolverResult(x, False, max_iter, abs(f(x)), "newton", trace)

    @staticmethod
    def secant(f, x0, x1, tolerance=1e-10, max_iter=100):
        """Solve a scalar root from two guesses without requiring a derivative."""
        trace = []
        f0, f1 = f(x0), f(x1)
        for i in range(1, max_iter + 1):
            denom = f1 - f0
            if abs(denom) < 1e-15:
                raise ValueError("zero_secant_denominator")
            x2 = x1 - f1 * (x1 - x0) / denom
            f2 = f(x2)
            trace.append({"iteration": i, "x": x2, "residual": abs(f2)})
            if abs(f2) <= tolerance or abs(x2 - x1) <= tolerance:
                return SolverResult(x2, True, i, abs(f2), "secant", trace)
            x0, x1, f0, f1 = x1, x2, f1, f2
        return SolverResult(x1, False, max_iter, abs(f1), "secant", trace)
