from aias_building_design_core import BuildingDesignCore
from aias_cad_professional import CADEngine
from aias_exchange_writers import ExchangeWriters

def test_dxf_pdf_write_and_validate(tmp_path):
    g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot")); cad=CADEngine().build(g,{}); w=ExchangeWriters(); d=w.write_dxf(cad,tmp_path/'A-101.dxf'); p=w.write_pdf(cad,tmp_path/'set.pdf')
    assert (tmp_path/'A-101.dxf').exists() and d['entities']>0; assert (tmp_path/'set.pdf').read_bytes().startswith(b'%PDF-1.4') and p['pages']==5
