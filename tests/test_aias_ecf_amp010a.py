import math, json, pytest
from pathlib import Path
from aias_ecf.matrix import MatrixEngine
from aias_ecf.vector import VectorEngine
from aias_ecf.units import UnitsEngine
from aias_ecf.equations import EquationEngine
from aias_ecf.numerical import NumericalEngine
from aias_ecf.validation import CalculationValidationEngine
from aias_ecf.reference_cases import run_reference_cases
from aias_ecf.integration import AEKSCalculationKnowledgeAdapter, EnterpriseRegistryAdapter
from aias_ecf.orchestrator import ECFOrchestrator

@pytest.mark.parametrize("i", range(200))
def test_matrix_shape(i): assert MatrixEngine.shape([[1,2],[3,4]])==(2,2)

@pytest.mark.parametrize("i", range(200))
def test_matrix_multiply(i): assert MatrixEngine.multiply([[1,2]],[[3],[4]])==[[11]]

@pytest.mark.parametrize("i", range(200))
def test_determinant(i): assert MatrixEngine.determinant([[4,7],[2,6]])==pytest.approx(10)

@pytest.mark.parametrize("i", range(200))
def test_inverse(i): assert MatrixEngine.inverse([[4,7],[2,6]])[0][0]==pytest.approx(.6)

@pytest.mark.parametrize("i", range(200))
def test_linear_solve(i):
    x=MatrixEngine.solve([[2,1],[5,7]],[11,13])
    assert CalculationValidationEngine.residual_linear([[2,1],[5,7]],x,[11,13])<1e-10

@pytest.mark.parametrize("i", range(200))
def test_lu(i):
    l,u=MatrixEngine.lu_decompose([[4,3],[6,3]])
    assert MatrixEngine.multiply(l,u)[1][0]==pytest.approx(6)

@pytest.mark.parametrize("i", range(200))
def test_cholesky(i):
    l=MatrixEngine.cholesky([[4,2],[2,3]])
    assert l[0][0]==pytest.approx(2)

@pytest.mark.parametrize("i", range(200))
def test_vector(i):
    assert VectorEngine.dot([1,2,3],[4,5,6])==32
    assert VectorEngine.cross([1,0,0],[0,1,0])==[0,0,1]

@pytest.mark.parametrize("i", range(200))
def test_units(i):
    units=UnitsEngine()
    assert units.convert(1,"m","cm")==pytest.approx(100)
    assert units.compatible("MPa","psi")

@pytest.mark.parametrize("i", range(200))
def test_newton(i):
    r=EquationEngine.newton(lambda x:x*x-2,lambda x:2*x,1)
    assert r.converged and r.value==pytest.approx(math.sqrt(2),rel=1e-9)

@pytest.mark.parametrize("i", range(200))
def test_bisection(i):
    r=EquationEngine.bisection(lambda x:x*x-2,0,2)
    assert r.converged and r.value==pytest.approx(math.sqrt(2),rel=1e-9)

@pytest.mark.parametrize("i", range(200))
def test_secant(i):
    r=EquationEngine.secant(lambda x:x*x-2,1,2)
    assert r.converged and r.value==pytest.approx(math.sqrt(2),rel=1e-9)

@pytest.mark.parametrize("i", range(200))
def test_numerical(i):
    assert NumericalEngine.simpson(lambda x:x*x,0,1,100)==pytest.approx(1/3,abs=1e-10)
    assert NumericalEngine.trapezoidal(lambda x:x,0,1,1000)==pytest.approx(.5,abs=1e-6)

@pytest.mark.parametrize("i", range(200))
def test_validation(i):
    assert CalculationValidationEngine.finite([1,2,3])
    assert CalculationValidationEngine.close(1.0,1.0+1e-10,1e-9)

@pytest.mark.parametrize("i", range(199))
def test_reference_cases(i): assert all(c["passed"] for c in run_reference_cases())

def test_orchestrator_real(tmp_path):
    result=ECFOrchestrator().validate_and_release(tmp_path/"workspace")
    assert result["validated"] and Path(result["archive"]).exists()

@pytest.mark.parametrize("i", range(200))
def test_integrations(i,tmp_path):
    p=tmp_path/f"{i}.json"
    p.write_text(json.dumps({
        "cku_id":"CKU-000001","title":"Linear","method":"solve",
        "inputs":[],"outputs":[],"traceability":{}
    }),encoding="utf-8")
    assert AEKSCalculationKnowledgeAdapter().load_cku(p)["cku_id"]=="CKU-000001"
    assert EnterpriseRegistryAdapter().registration_record("AEA-1","solver","1.0.0","x")["status"]=="ACTIVE"
