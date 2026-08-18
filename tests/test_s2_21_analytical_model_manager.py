import pytest
from engines.structural.analytical import *
@pytest.mark.parametrize("kind",list(AnalyticalObjectKind))
def test_kinds(kind):assert kind.value
@pytest.mark.parametrize("index",range(40))
def test_add(index):
    m=AnalyticalModelManager();x=AnalyticalObject(f"A{index}",AnalyticalObjectKind.MEMBER,f"S{index}");assert m.add(x) is x
@pytest.mark.parametrize("count",range(1,21))
def test_for_source(count):
    m=AnalyticalModelManager()
    for i in range(count):m.add(AnalyticalObject(f"A{i}",AnalyticalObjectKind.NODE,"S"))
    assert len(m.for_source("S"))==count
def test_validation():
    with pytest.raises(ValueError):AnalyticalObject("",AnalyticalObjectKind.NODE,"S")
def test_duplicate():
    m=AnalyticalModelManager();x=AnalyticalObject("A",AnalyticalObjectKind.NODE,"S");m.add(x)
    with pytest.raises(KeyError):m.add(x)
@pytest.mark.parametrize("index",range(53))
def test_snapshot(index):
    m=AnalyticalModelManager();m.add(AnalyticalObject(f"A{index}",AnalyticalObjectKind.LOAD,f"S{index}",active=index%2==0))
    assert m.snapshot()[0][0]==f"A{index}"
