"""Numerical integration, differentiation and interpolation primitives."""
from __future__ import annotations

class NumericalEngine:
    """Expose validated trapezoidal, Simpson, central-difference and linear methods."""
    @staticmethod
    def trapezoidal(f, a, b, n=1000):
        """Integrate a scalar function using a positive number of trapezoids."""
        if n <= 0: raise ValueError("n_must_be_positive")
        h = (b - a) / n
        return h * (0.5*f(a) + sum(f(a+i*h) for i in range(1,n)) + 0.5*f(b))

    @staticmethod
    def simpson(f, a, b, n=1000):
        """Integrate a scalar function using an even number of Simpson intervals."""
        if n <= 0 or n % 2:
            raise ValueError("n_must_be_positive_even")
        h = (b - a) / n
        total = f(a) + f(b)
        total += 4 * sum(f(a+i*h) for i in range(1,n,2))
        total += 2 * sum(f(a+i*h) for i in range(2,n,2))
        return total * h / 3.0

    @staticmethod
    def derivative(f, x, h=1e-6):
        """Estimate a first derivative by a central finite difference."""
        if h <= 0: raise ValueError("h_must_be_positive")
        return (f(x+h) - f(x-h)) / (2*h)

    @staticmethod
    def linear_interpolate(x0, y0, x1, y1, x):
        """Interpolate or extrapolate linearly between two distinct abscissae."""
        if x1 == x0: raise ValueError("duplicate_x")
        return y0 + (y1-y0)*(x-x0)/(x1-x0)
