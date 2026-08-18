from aias_building_design_core import BuildingDesignCore
from aias_cad_professional import CADEngine
from aias_dxf_writer import ValidDxfWriter
def test_dxf_has_required_sections(tmp_path):
 d=CADEngine().build(BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project('p'))); p=tmp_path/'x.dxf'; m=ValidDxfWriter().write(d,p); assert not ValidDxfWriter().validate(p.read_text()) and m
