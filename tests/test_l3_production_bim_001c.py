"""L3-PRODUCTION-BIM-001C contract tests."""
from pathlib import Path
import json,sys,types
from aias_l3_production_bim.authority_binding import NativeAuthorityRegistry
from aias_l3_production_bim.native_project_integration import NativeProjectIntegrationService
def _disc(tmp_path:Path):
    m=types.ModuleType("aias_test_native_authorities")
    class L:
        def __init__(self):self.items=[]
        def add_level(self,name,elevation,**kw):self.items.append((name,elevation));return self.items[-1]
    class G:
        def __init__(self):self.items=[]
        def add_grid(self,name,start,end,**kw):self.items.append((name,start,end));return self.items[-1]
    class V:
        def __init__(self):self.items=[]
        def add_view(self,name,view_type,**kw):self.items.append((name,view_type));return self.items[-1]
    class D:
        def __init__(self):self.items=[]
        def add_sheet(self,number,name):self.items.append((number,name));return self.items[-1]
    m.L=L;m.G=G;m.V=V;m.D=D;sys.modules[m.__name__]=m
    row=lambda s:{"module":m.__name__,"symbol":s,"path":"synthetic.py","score":100}
    p=tmp_path/"DISCOVERY.json";p.write_text(json.dumps({"authority_map":{"levels":[row("L")],"grids":[row("G")],"views":[row("V")],"documentation":[row("D")]}}));return p
def test_registry_resolves_native_authorities(tmp_path):
    """Resolve compatible discovered authorities."""
    r=NativeAuthorityRegistry(_disc(tmp_path));b=r.resolve();assert b["levels"].resolved and "add_level" in b["levels"].compatible_operations
def test_mirror_level_grid_view_sheet(tmp_path):
    """Mirror project document operations while preserving canonical state."""
    s=NativeProjectIntegrationService("P",discovery_path=_disc(tmp_path));s.start();l=s.add_level("L1",0);s.add_grid("A",(0,0),(0,10));v=s.add_plan_view("Plan",l.id);s.add_sheet("A101","Plan",[v.id]);r=s.native_binding_report();assert all(r["mirrored_operations"][d]==1 for d in ("levels","grids","views","documentation"))
def test_safe_fallback_for_incompatible_contract(tmp_path):
    """Keep canonical state when native call signature is incompatible."""
    p=_disc(tmp_path);d=json.loads(p.read_text());d["authority_map"]["levels"][0]["symbol"]="G";p.write_text(json.dumps(d));s=NativeProjectIntegrationService("P",discovery_path=p);s.start();l=s.add_level("L1",0);assert l.id in s.state.levels and s.native_binding_report()["mirrored_operations"]["levels"]==0
def test_preserves_native_bim_authoring(tmp_path):
    """Retain certified Level 2 native wall authoring."""
    s=NativeProjectIntegrationService("P",discovery_path=_disc(tmp_path));s.start();l=s.add_level("L1",0);w=s.create_wall((0,0),(5,0),level_id=l.id);assert w.id in s.vertical_service.state.walls
