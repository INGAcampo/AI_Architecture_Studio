from pathlib import Path
from aias_l2_vertical_slice import AUTHORITY_MAP,AuthorityResolver,VerticalSliceService
from aias_l2_vertical_slice.service import VerticalSliceError

def build_service():
    s=VerticalSliceService()
    walls=[
        s.create_wall((0,0),(8,0)),
        s.create_wall((8,0),(8,6)),
        s.create_wall((8,6),(0,6)),
        s.create_wall((0,6),(0,0)),
    ]
    return s,walls

def test_authority_contract_has_all_domains():
    assert set(AUTHORITY_MAP)=={"wall","door","window","room","properties","relationships","history","persistence","workspace2","selection"}
    rows=AuthorityResolver().audit()
    assert len(rows)==10

def test_full_vertical_slice_round_trip(tmp_path):
    s,walls=build_service()
    door=s.add_opening("door",walls[0].id,1.0,0.9,2.1)
    window=s.add_opening("window",walls[1].id,2.0,1.5,1.2,0.9)
    room=s.create_room([w.id for w in walls],"Room 101")
    s.set_property(walls[0].id,"level","Level 1")
    assert s.state.openings[door.id].properties["level"]=="Level 1"
    s.select(walls[0].id,door.id,window.id,room.id)
    path=s.save(tmp_path/"project.aias.json")
    loaded=VerticalSliceService.load(path)
    assert loaded.state.to_dict()==s.state.to_dict()
    projection=loaded.workspace_projection()
    assert [row["category"] for row in projection["tree"]]==["Walls","Openings","Rooms"]
    assert len(projection["selection"])==4

def test_undo_redo_restores_property_and_relationship_state():
    s,walls=build_service()
    door=s.add_opening("door",walls[0].id,1.0,0.9,2.1)
    revision=s.state.revision
    s.set_property(walls[0].id,"level","Level 2")
    assert s.state.openings[door.id].properties["level"]=="Level 2"
    assert s.undo()
    assert "level" not in s.state.walls[walls[0].id].properties
    assert s.state.revision==revision
    assert s.redo()
    assert s.state.walls[walls[0].id].properties["level"]=="Level 2"

def test_invariants_are_enforced():
    s,walls=build_service()
    try:s.add_opening("door",walls[0].id,7.5,1.0,2.1)
    except VerticalSliceError as exc:assert str(exc)=="opening_outside_wall"
    else:raise AssertionError("expected VerticalSliceError")
