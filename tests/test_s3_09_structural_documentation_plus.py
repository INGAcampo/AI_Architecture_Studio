import pytest
from engines.structural.systems.documentation_plus import *
from engines.structural.systems.load_cases import *

@pytest.mark.parametrize("i",range(120))
def test_doc_plus(i):
    d=LoadCase(f"D{i}","Dead",LoadCategory.DEAD,1.0,{})
    r=StructuralDocumentationPlus().load_report((d,),())
    assert r.summary["cases"]==1
    assert r.rows[0][0]==f"D{i}"
