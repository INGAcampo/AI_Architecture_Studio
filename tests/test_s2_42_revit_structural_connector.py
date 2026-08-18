import pytest
from engines.structural.revit_connector import *
@pytest.mark.parametrize("index",range(120))
def test_revit_connector(index):
    c=RevitStructuralConnector();e=RevitStructuralElement(f"E{index}","Structural Framing","W310",{"Mark":str(index)})
    restored=c.import_json(c.export_json("AIAS",(e,)))
    assert restored[0].element_id==e.element_id
