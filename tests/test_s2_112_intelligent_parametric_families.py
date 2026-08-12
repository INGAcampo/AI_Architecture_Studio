import pytest
from engines.ai.families import *
@pytest.mark.parametrize("i",range(120))
def test_family(i):
    f=FamilyDefinition(f"door{i}",(FamilyParameter("width",0.9),FamilyParameter("mark","",False)),(FamilyType("900x2100",{"width":0.9}),))
    inst=FamilyInstance(f"I{i}",f,f.types[0],{"mark":f"D{i}"})
    assert inst.value("width")==0.9 and inst.value("mark")==f"D{i}"
