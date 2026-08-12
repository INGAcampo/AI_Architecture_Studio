"""L3-PRODUCTION-BIM-001B contract tests."""
from aias_l3_production_bim.project_core import ProjectDocumentState
from aias_l3_production_bim.service import NativeProjectAuthoringService,ProjectAuthoringError

def _p():
    s=NativeProjectAuthoringService("Lighthouse",project_number="L3-001"); s.start(); return s

def test_project_document_roundtrip():
    """Round-trip levels, grids, views and sheets."""
    s=_p(); l=s.add_level("Level 1",0); s.add_grid("A",(0,0),(0,10)); v=s.add_plan_view("Plan",l.id); sh=s.add_sheet("A101","Plan",[v.id])
    d=s.state.to_dict(); assert ProjectDocumentState.from_dict(d).to_dict()==d; assert sh.view_ids==[v.id]

def test_native_bim_under_project_level():
    """Author native walls, openings and room under one level."""
    s=_p(); l=s.add_level("Level 1",0)
    w=[s.create_wall((0,0),(6,0),level_id=l.id),s.create_wall((6,0),(6,4),level_id=l.id),s.create_wall((6,4),(0,4),level_id=l.id),s.create_wall((0,4),(0,0),level_id=l.id)]
    d=s.create_door(w[0].id,1,.9,2.1); n=s.create_window(w[1].id,1,1.2,1.2,.9); r=s.create_room([x.id for x in w],name="Office")
    assert s.vertical_service.state.walls[w[0].id].properties["level_id"]==l.id; assert d.id in s.vertical_service.state.openings; assert n.id in s.vertical_service.state.openings; assert r.id in s.vertical_service.state.rooms

def test_workspace_projection_and_selection():
    """Combine project hierarchy with native Workspace 2 selection."""
    s=_p(); l=s.add_level("Level 1",0); v=s.add_plan_view("Plan",l.id); w=s.create_wall((0,0),(5,0),level_id=l.id); s.select_object(w.id); p=s.workspace_projection()
    assert l.id in p["levels"] and v.id in p["views"]; assert p["bim"]["state"]["selected_node_id"]==f"instance.{w.id}"

def test_project_history_and_invariants():
    """Validate project Undo/Redo and document invariants."""
    s=_p(); s.add_level("Level 1",0); s.add_grid("A",(0,0),(0,10)); assert s.undo_project(); assert not s.state.grids; assert s.redo_project()
    try:s.add_level("Level 1",3)
    except ProjectAuthoringError:pass
    else:raise AssertionError("duplicate level must fail")

def test_project_save_reopen(tmp_path):
    """Persist and reopen project plus native BIM state."""
    s=_p(); l=s.add_level("Level 1",0); s.add_grid("A",(0,0),(0,10)); s.add_plan_view("Plan",l.id); w=s.create_wall((0,0),(5,0),level_id=l.id); s.select_object(w.id)
    a=s.state.to_dict(); b=s.vertical_service.state.to_dict(); path=s.save(tmp_path/"project.aias.json"); assert not s.dirty; s.add_view("Temp","3d"); assert s.dirty; s.reopen(path); assert s.state.to_dict()==a; assert s.vertical_service.state.to_dict()==b; assert not s.dirty
