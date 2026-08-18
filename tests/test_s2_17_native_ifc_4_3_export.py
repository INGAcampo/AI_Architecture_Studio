import json, pytest
from engines.interoperability.ifc import *
@pytest.mark.parametrize("kind",list(IfcEntityKind))
def test_kinds(kind): assert kind.value.startswith("Ifc")
@pytest.mark.parametrize("index",range(30))
def test_add_entities(index):
    e=NativeIfc43ExportEngine(); x=IfcEntity(f"G{index}",IfcEntityKind.WALL,f"Wall {index}"); assert e.add(x) is x
@pytest.mark.parametrize("index",range(20))
def test_json_export(index):
    e=NativeIfc43ExportEngine(); e.add(IfcEntity(f"G{index}",IfcEntityKind.BEAM,f"Beam {index}",{"i":index}))
    data=json.loads(e.export_json()); assert data["schema"]=="IFC4X3"; assert data["entities"][0]["properties"]["i"]==index
@pytest.mark.parametrize("index",range(20))
def test_step_export(index):
    e=NativeIfc43ExportEngine(); e.add(IfcEntity(f"G{index}",IfcEntityKind.COLUMN,f"Column {index}"))
    text=e.export_step(); assert "IFC4X3" in text; assert "IFCCOLUMN" in text
def test_validation():
    with pytest.raises(ValueError): IfcEntity("",IfcEntityKind.WALL,"Wall")
def test_duplicate():
    e=NativeIfc43ExportEngine(); x=IfcEntity("G",IfcEntityKind.WALL,"Wall");e.add(x)
    with pytest.raises(KeyError):e.add(x)
@pytest.mark.parametrize("index",range(34))
def test_relationship_cases(index):
    x=IfcEntity(f"G{index}",IfcEntityKind.SLAB,f"Slab {index}",relationships=(f"S{index}",));assert x.relationships[0]==f"S{index}"
