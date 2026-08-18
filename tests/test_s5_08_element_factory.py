import pytest
from engines.fem.factory import *

@pytest.mark.parametrize("i",range(120))
def test_factory(i):
    e=FiniteElementFactory().create("truss",element_id=f"T{i}",node_ids=("N1","N2"),start=(0,0,0),end=(1,0,0),area=0.01,elastic_modulus=200e9)
    assert e.element_id==f"T{i}"
    with pytest.raises(KeyError): FiniteElementFactory().create("unknown")
