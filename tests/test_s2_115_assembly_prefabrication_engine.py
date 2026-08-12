import pytest
from engines.ai.prefabrication import *
@pytest.mark.parametrize("i",range(120))
def test_prefab(i):
    a=AssemblyDefinition(f"A{i}",(AssemblyPart("beam",2,10),AssemblyPart("plate",4,2)))
    e=PrefabricationEngine();assert e.total_parts(a)==6 and e.total_mass(a)==28 and e.bill_of_materials(a)["plate"]==4
