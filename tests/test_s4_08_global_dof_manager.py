import pytest
from engines.structural.core.nodes import StructuralNode,NodeRestraint
from engines.numerical.dof import *

@pytest.mark.parametrize("i", range(120))
def test_dof(i):
    nodes=(StructuralNode("N1",0,0,0,NodeRestraint(True,True,True,True,True,True)),StructuralNode("N2",1,0,0))
    m=GlobalDofManager().build(nodes)
    assert m.free_count==6
    assert m.restrained_count==6
    assert m.equation_by_node_dof[("N1","ux")] is None
