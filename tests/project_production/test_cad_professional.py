from aias_building_design_core import BuildingDesignCore
from aias_cad_professional import CADEngine

def test_cad_document_has_traceable_primitives_and_sheets():
    g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot")); d=CADEngine().build(g,{})
    assert not CADEngine().validate(d); assert len(d.views)==5 and len(d.sheets)==5
    assert any(e["kind"]=="dimension" for e in d.entities); assert all(len(s["sha256"])==64 for s in d.sheets)

def test_cad_fails_closed_without_graph():
    try: CADEngine().build(BuildingDesignCore().create_project("x"))
    except ValueError: pass
    else: raise AssertionError("expected missing graph failure")
