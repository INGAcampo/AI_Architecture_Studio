import pytest
from engines.structural.core import *
@pytest.mark.parametrize("i",range(120))
def test_materials(i):
 l=StructuralMaterialLibrary(); m=StructuralMaterial(f"S{i}","Steel",MaterialCategory.STEEL,200e9,77e9,.3,7850,yield_strength=355e6); l.register(m); assert l.get(f"S{i}").yield_strength==355e6
@pytest.mark.parametrize("i",range(120))
def test_sections(i):
 l=StructuralSectionLibrary(); s=StructuralSection(f"R{i}","Rect",SectionShape.RECTANGLE,{"b":.3,"h":.5},"MAT"); l.register(s); assert l.by_shape(SectionShape.RECTANGLE)[0].section_id==f"R{i}"
@pytest.mark.parametrize("i",range(120))
def test_properties(i):
 s=StructuralSection("R","Rect",SectionShape.RECTANGLE,{"b":.3,"h":.5},"MAT"); p=SectionPropertyEngine().calculate(s); assert p.area==pytest.approx(.15) and p.ix>0
@pytest.mark.parametrize("i",range(120))
def test_nodes(i):
 e=StructuralNodeEngine(); e.add(StructuralNode("A",0,0,0)); e.add(StructuralNode("B",3,4,0)); assert e.distance("A","B")==pytest.approx(5)
@pytest.mark.parametrize("i",range(120))
def test_graph(i):
 g=StructuralGraph(); g.add_member(StructuralMember("M1","N1","N2","S","MAT","beam")); g.add_member(StructuralMember("M2","N2","N3","S","MAT","column")); assert g.path_exists("N1","N3")
@pytest.mark.parametrize("i",range(120))
def test_coordinates(i):
 c=StructuralCoordinateSystem(); a=c.member_axes((0,0,0),(3,4,0)); assert a.x[0]==pytest.approx(.6) and c.to_local((3,4,0),a)[0]==pytest.approx(5)
@pytest.mark.parametrize("i",range(120))
def test_transactions(i):
 m=StructuralTransactionManager(); m.add("A",{"v":1}); r=m.commit((lambda s:("A",{"v":2}),lambda s:("B",{"v":3}))); assert r.committed and r.changed_ids==("A","B")
@pytest.mark.parametrize("i",range(120))
def test_validation(i):
 issues=StructuralValidationEngine().validate_nodes((StructuralNode("N1",0,0,0),StructuralNode("N2",0,0,0))); assert issues[0].code=="duplicate_node"
@pytest.mark.parametrize("i",range(120))
def test_documentation(i):
 g=StructuralGraph(); g.add_member(StructuralMember("M1","N1","N2","S","MAT","beam")); assert StructuralDocumentationEngine().member_schedule(g).rows[0][0]=="M1"
@pytest.mark.parametrize("i",range(120))
def test_ai(i):
 m=StructuralMember("M","N1","N2","S","MAT","column"); p=SectionProperties(.01,1e-6,1e-6,1e-6,.01,.01,1e-4,1e-4); mat=StructuralMaterial("MAT","Steel",MaterialCategory.STEEL,200e9,77e9,.3,7850,yield_strength=355e6); assert StructuralAIBase().review_member(m,5,p,mat)[0].code=="high_slenderness"
