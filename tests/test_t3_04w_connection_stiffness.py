import pytest
from design.steel.connection_stiffness import *
@pytest.mark.parametrize("i",range(120))
def test_stiffness(i):
    assert ConnectionStiffnessEngine().classify(100,.01,1000).classification=="rigid"
