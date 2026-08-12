import pytest
from dataclasses import dataclass
from engines.structural.systems.regeneration import *

@dataclass(frozen=True)
class Obj:
    member_id:str
    value:int

@pytest.mark.parametrize("i",range(120))
def test_regeneration(i):
    e=StructuralRegenerationEngine()
    r=e.regenerate(Obj(f"M{i}",2),1,{"double":lambda o:o.value*2})
    assert r.object_id==f"M{i}"
    assert r.outputs["double"]==4
    assert r.new_revision==1
