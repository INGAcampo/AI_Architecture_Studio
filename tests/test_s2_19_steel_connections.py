import pytest
from engines.structural.connections import *
@pytest.mark.parametrize("kind",list(ConnectionKind))
def test_kinds(kind):assert kind.value
@pytest.mark.parametrize("r,c",[(1,1),(2,1),(2,2),(3,2),(4,2),(4,3),(5,2),(6,2),(6,3),(8,4)])
def test_bolt_count(r,c):assert BoltGroup(r,c,.02,.08,.08).count==r*c
@pytest.mark.parametrize("index",range(30))
def test_add(index):
    e=SteelConnectionEngine();x=SteelConnection(f"C{index}",ConnectionKind.END_PLATE,("B","C"),.01,BoltGroup(2,2,.02,.08,.08));assert e.add(x) is x
@pytest.mark.parametrize("t", [.006,.008,.01,.012,.015,.018,.02,.025,.03,.04])
def test_plate_volume(t):
    e=SteelConnectionEngine();e.add(SteelConnection("C",ConnectionKind.BASE_PLATE,("C","F"),t,BoltGroup(2,2,.02,.1,.1)))
    assert e.plate_volume("C",.4,.4)==pytest.approx(.16*t)
def test_validation():
    with pytest.raises(ValueError):BoltGroup(0,1,.02,.1,.1)
@pytest.mark.parametrize("index",range(64))
def test_connection_properties(index):
    c=SteelConnection(f"C{index}",ConnectionKind.SPLICE,("A","B"),.01+index*.0001,BoltGroup(2,2,.02,.08,.08));assert c.plate_thickness>0
