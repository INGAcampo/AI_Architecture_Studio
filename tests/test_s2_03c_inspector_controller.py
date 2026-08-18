import pytest
from engines.property import IfcMapping,PropertyDefinition,PropertyGroup,PropertyService,PropertyType,SharedParameter,SharedParameterLibrary
from gui.inspector.controller import InspectorController,InspectorFilter,InspectorProperty
class E:
    def __init__(self):self.id='wall-01';self.name='Wall 01';self.height=3.0;self.properties={'Thickness':0.20,'Material':'Concrete'}
    def info(self):return {'Nombre':self.name,'Altura':self.height,'Propiedades':dict(self.properties)}
def test_search():
    p=InspectorProperty('FireRating','Resistencia al fuego','120 min',group='Identity');assert p.matches('fuego') and p.matches('120') and not p.matches('concreto')
def test_groups():
    c=InspectorController();c.inspect(E());g=c.grouped();assert {'Geometry','Materials','Identity'}<=set(g)
def test_native_edit():
    e=E();c=InspectorController();c.inspect(e);c.update('Thickness',0.25);assert e.properties['Thickness']==0.25;assert c.query(active_filter=InspectorFilter.MODIFIED)[0].name=='Thickness'
def test_service_override():
    s=PropertyService();s.register_definition(PropertyDefinition('Thickness',PropertyType.LENGTH,group=PropertyGroup.GEOMETRY,unit='m'));s.bind('wall-01','Thickness',0.30);c=InspectorController(s);c.inspect(E());c.update('Thickness',0.35);assert s.get_value('wall-01','Thickness')==0.35
def test_read_only():
    s=PropertyService();s.register_definition(PropertyDefinition('Area',PropertyType.AREA,read_only=True));s.bind('wall-01','Area',12.0);c=InspectorController(s);c.inspect(E());p=next(x for x in c.properties if x.name=='Area');assert not p.editable
    with pytest.raises(PermissionError):p.set_value(14.0)
def test_shared_filter():
    s=PropertyService();s.register_definition(PropertyDefinition('AssetCode',PropertyType.TEXT));s.bind('wall-01','AssetCode','W-001',source='shared');c=InspectorController(s);c.inspect(E());assert [x.name for x in c.query(active_filter=InspectorFilter.SHARED)]==['AssetCode']
def test_ifc_filter():
    s=PropertyService();s.register_definition(PropertyDefinition('FireRating',PropertyType.TEXT));s.bind('wall-01','FireRating','120 min',source='shared');lib=SharedParameterLibrary();lib.register(SharedParameter(guid='fire',definition=PropertyDefinition('FireRating',PropertyType.TEXT),ifc_mapping=IfcMapping('Pset_WallCommon','FireRating')));c=InspectorController(s,lib);c.inspect(E());assert [x.name for x in c.query(active_filter=InspectorFilter.IFC)]==['FireRating']
def test_combined_filter():
    c=InspectorController();c.inspect(E());assert [x.name for x in c.query('thick',InspectorFilter.EDITABLE)]==['Thickness']
def test_clear():
    c=InspectorController();c.inspect(E());c.clear();assert c.element is None and c.properties==()
def test_unknown():
    c=InspectorController();c.inspect(E())
    with pytest.raises(KeyError):c.update('unknown',1)
