import pytest
from engines.fem.shell import *

@pytest.mark.parametrize("i",range(120))
def test_shell(i):
    e=ShellElement4(f"S{i}",("N1","N2","N3","N4"),10,0.15,25e9,0.2)
    assert e.membrane_stiffness()>e.bending_stiffness()
    assert len(e.local_stiffness_matrix())==8
