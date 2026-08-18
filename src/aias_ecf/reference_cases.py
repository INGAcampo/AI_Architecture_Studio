"""Mathematical reference cases spanning matrices, units, roots and integration."""
from __future__ import annotations
import math
from .matrix import MatrixEngine
from .units import UnitsEngine
from .equations import EquationEngine
from .numerical import NumericalEngine
from .validation import CalculationValidationEngine

def run_reference_cases():
    """Execute deterministic kernel checks with numerical residual tolerances."""
    cases = []
    x = MatrixEngine.solve([[2,1],[5,7]],[11,13])
    cases.append({"id":"MC-000001","passed":CalculationValidationEngine.residual_linear([[2,1],[5,7]],x,[11,13]) < 1e-10})
    cases.append({"id":"MC-000002","passed":abs(MatrixEngine.determinant([[4,7],[2,6]])-10.0)<1e-10})
    inv = MatrixEngine.inverse([[4,7],[2,6]])
    cases.append({"id":"MC-000003","passed":abs(inv[0][0]-0.6)<1e-10})
    cases.append({"id":"MC-000004","passed":abs(UnitsEngine().convert(1,"m","ft")-3.280839895013123)<1e-10})
    n = EquationEngine.newton(lambda t:t*t-2, lambda t:2*t, 1.0)
    cases.append({"id":"MC-000005","passed":abs(n.value-math.sqrt(2))<1e-9})
    b = EquationEngine.bisection(lambda t:t*t-2,0,2)
    cases.append({"id":"MC-000006","passed":abs(b.value-math.sqrt(2))<1e-9})
    s = NumericalEngine.simpson(lambda t:t*t,0,1,100)
    cases.append({"id":"MC-000007","passed":abs(s-1/3)<1e-10})
    return cases
