import pytest
from engines.structural.analysis import *
@pytest.mark.parametrize("E,A,L",[(200e9,.01,1),(210e9,.005,2),(70e9,.02,3),(30e9,.1,4),(10e9,.2,5)]*4)
def test_axial_stiffness(E,A,L):
    k=axial_stiffness(E,A,L); assert k[0][0]==pytest.approx(E*A/L); assert k[0][1]==-k[0][0]
@pytest.mark.parametrize("index",range(30))
def test_add_nodes(index):
    e=StructuralAnalysisCore();n=AnalysisNode(f"N{index}",index,0,0);assert e.add_node(n) is n
@pytest.mark.parametrize("length",range(1,21))
def test_element_lengths(length):
    e=StructuralAnalysisCore();e.add_node(AnalysisNode("A",0,0,0));e.add_node(AnalysisNode("B",length,0,0))
    e.add_element(BarElement("E","A","B",.01,200e9));assert e.length("E")==length
@pytest.mark.parametrize("length",range(1,21))
def test_element_stiffness(length):
    e=StructuralAnalysisCore();e.add_node(AnalysisNode("A",0,0,0));e.add_node(AnalysisNode("B",length,0,0))
    e.add_element(BarElement("E","A","B",.01,200e9));assert e.stiffness("E")[0][0]==pytest.approx(2e9/length)
def test_validation():
    with pytest.raises(ValueError):AnalysisNode("",0,0,0)
def test_missing_node():
    e=StructuralAnalysisCore()
    with pytest.raises(KeyError):e.add_element(BarElement("E","A","B",.01,1))
@pytest.mark.parametrize("index",range(28))
def test_diagonal_lengths(index):
    e=StructuralAnalysisCore();e.add_node(AnalysisNode("A",0,0,0));e.add_node(AnalysisNode("B",index+1,index+1,0))
    e.add_element(BarElement("E","A","B",.01,1));assert e.length("E")>0
