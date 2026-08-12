import pytest
from dataclasses import dataclass
from engines.analysis.project import *

@dataclass
class Obj: node_id:str
@dataclass
class Elem: element_id:str

@pytest.mark.parametrize("i",range(120))
def test_project(i):
    p=AnalysisProject(f"P{i}","Demo")
    p.add_node(Obj("N1")); p.add_element(Elem("E1"))
    assert p.summary()["nodes"]==1
    assert p.summary()["elements"]==1
