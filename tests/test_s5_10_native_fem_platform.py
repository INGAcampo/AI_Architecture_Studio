import pytest
from engines.fem.platform import *
from engines.fem.assembly import FEMAssemblyEngine
from engines.fem.truss import TrussElement
from engines.numerical.vectors import DenseVector

@pytest.mark.parametrize("i",range(120))
def test_native_fem(i):
    e=TrussElement(f"T{i}",("N1","N2"),(0,0,0),(1,0,0),1.0,100.0)
    p=NativeFEMPlatform(FEMAssemblyEngine())
    r=p.analyze(1,{e.element_id:(None,0)},(e,),DenseVector((10.0,)))
    assert r.displacements.values[0]==pytest.approx(0.1)
    assert r.equilibrium_ok
