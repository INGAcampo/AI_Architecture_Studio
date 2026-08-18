import pytest
from engines.analysis.results_db import *

@pytest.mark.parametrize("i",range(120))
def test_db(i):
    db=StructuralResultsDatabase()
    db.store_node_result("LC1","N1",{"ux":1})
    db.store_element_result("LC1",f"E{i}",{"n":10})
    assert db.get_node_result("LC1","N1")["ux"]==1
    assert db.cases()==("LC1",)
