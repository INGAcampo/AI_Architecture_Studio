"""Compose Level 3 project authoring with the certified Level 2 native BIM stack."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import hashlib, json
from aias_l2_vertical_slice.live_workspace import LiveWorkspaceSession
from aias_l2_vertical_slice.native_integration import NativeVerticalSliceBridge
from aias_l2_vertical_slice.service import VerticalSliceService
from .project_core import Grid,Level,ProjectDocumentState,ProjectInfo,ProjectView,Sheet

class ProjectAuthoringError(RuntimeError):
    """Raised when a project operation violates an authoring invariant."""

class NativeProjectAuthoringService:
    """Coordinate project lifecycle, document objects and native BIM authoring."""
    def __init__(self,name:str,project_number:str="",description:str="",units:str="metric",**ui):
        self.state=ProjectDocumentState(ProjectInfo(name,project_number,description,units))
        self.vertical_service=VerticalSliceService()
        self.bridge=NativeVerticalSliceBridge(self.vertical_service)
        self.live=LiveWorkspaceSession(self.bridge,property_inspector=ui.get("property_inspector"),workspace_widget=ui.get("workspace_widget"),visual_selection=ui.get("visual_selection"))
        self._started=False; self._saved=None; self._history=[]; self._redo=[]
    def start(self):
        """Start native Workspace 2 synchronization."""
        self.live.start(); self._started=True; self._saved=self._fingerprint()
    def add_level(self,name,elevation,**properties):
        """Create a unique project level."""
        self._ready()
        if any(x.name==name for x in self.state.levels.values()): raise ProjectAuthoringError("duplicate_level_name:"+name)
        self._checkpoint(); x=Level(name,float(elevation),properties=properties); self.state.levels[x.id]=x; self.state.revision+=1; return x
    def add_grid(self,name,start,end,**properties):
        """Create a non-zero project grid."""
        self._ready()
        if start==end: raise ProjectAuthoringError("zero_length_grid")
        if any(x.name==name for x in self.state.grids.values()): raise ProjectAuthoringError("duplicate_grid_name:"+name)
        self._checkpoint(); x=Grid(name,tuple(start),tuple(end),properties=properties); self.state.grids[x.id]=x; self.state.revision+=1; return x
    def add_view(self,name,view_type,level_id=None,**properties):
        """Create a named project view."""
        self._ready()
        if level_id is not None: self._level(level_id)
        if any(x.name==name for x in self.state.views.values()): raise ProjectAuthoringError("duplicate_view_name:"+name)
        self._checkpoint(); x=ProjectView(name,view_type,level_id,properties=properties); self.state.views[x.id]=x
        if self.state.active_view_id is None:self.state.active_view_id=x.id
        self.state.revision+=1; return x
    def add_plan_view(self,name,level_id):
        """Create a floor plan bound to a level."""
        return self.add_view(name,"plan",level_id=level_id)
    def add_sheet(self,number,name,view_ids=None):
        """Create a drawing sheet and validate placed views."""
        self._ready()
        if any(x.number==number for x in self.state.sheets.values()): raise ProjectAuthoringError("duplicate_sheet_number:"+number)
        ids=list(view_ids or [])
        for i in ids:self._view(i)
        self._checkpoint(); x=Sheet(number,name,ids); self.state.sheets[x.id]=x; self.state.revision+=1; return x
    def place_view_on_sheet(self,sheet_id,view_id):
        """Place a project view on a sheet."""
        sh=self._sheet(sheet_id); self._view(view_id)
        if view_id not in sh.view_ids:self._checkpoint(); sh.view_ids.append(view_id); self.state.revision+=1
    def create_wall(self,*a,level_id=None,**kw):
        """Create a native BIM wall hosted by an optional project level."""
        p=dict(kw.pop("properties",{}))
        if level_id is not None:
            l=self._level(level_id); p["level_id"]=level_id; p.setdefault("level",l.name)
        return self.live.create_wall(*a,properties=p,**kw)
    def create_door(self,*a,**kw):
        """Create a native hosted door."""
        return self.live.create_door(*a,**kw)
    def create_window(self,*a,**kw):
        """Create a native hosted window."""
        return self.live.create_window(*a,**kw)
    def create_room(self,*a,**kw):
        """Create a native room."""
        return self.live.create_room(*a,**kw)
    def select_object(self,object_id):
        """Synchronize object selection to Workspace 2."""
        self.live.select_object(object_id); self.state.selected_object_ids=[] if object_id is None else [object_id]
    def workspace_projection(self):
        """Return combined project and native BIM Workspace 2 state."""
        return {"project":self.state.project.name,"levels":list(self.state.levels),"grids":list(self.state.grids),"views":list(self.state.views),"sheets":list(self.state.sheets),"active_view_id":self.state.active_view_id,"bim":self.bridge.workspace_snapshot()}
    def undo_project(self):
        """Undo a project-document transaction."""
        if not self._history:return False
        self._redo.append(self.state.clone()); self.state=self._history.pop(); return True
    def redo_project(self):
        """Redo a project-document transaction."""
        if not self._redo:return False
        self._history.append(self.state.clone()); self.state=self._redo.pop(); return True
    def save(self,path:Path):
        """Persist project document plus native BIM."""
        self._ready(); path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); native=path.with_suffix(path.suffix+".native.json"); self.live.save(native)
        path.write_text(json.dumps({"schema":"aias.l3.production-bim.project.v1","project_state":self.state.to_dict(),"native_bim_file":native.name},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n"); self._saved=self._fingerprint(); return path
    def reopen(self,path:Path):
        """Reopen project document plus native BIM."""
        self._ready(); path=Path(path); env=json.loads(path.read_text(encoding="utf-8-sig"))
        if env.get("schema")!="aias.l3.production-bim.project.v1": raise ProjectAuthoringError("unsupported_project_schema")
        self.state=ProjectDocumentState.from_dict(env["project_state"]); self.live.reopen(path.parent/env["native_bim_file"]); self._saved=self._fingerprint()
    @property
    def dirty(self):
        """Return whether project/native state differs from checkpoint."""
        return self._saved is None or self._saved!=self._fingerprint()
    def _checkpoint(self):
        self._history.append(self.state.clone()); self._redo.clear()
    def _level(self,i):
        if i not in self.state.levels:raise ProjectAuthoringError("unknown_level:"+i)
        return self.state.levels[i]
    def _view(self,i):
        if i not in self.state.views:raise ProjectAuthoringError("unknown_view:"+i)
        return self.state.views[i]
    def _sheet(self,i):
        if i not in self.state.sheets:raise ProjectAuthoringError("unknown_sheet:"+i)
        return self.state.sheets[i]
    def _fingerprint(self):
        raw=json.dumps({"project":self.state.to_dict(),"bim":self.vertical_service.state.to_dict()},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
        return hashlib.sha256(raw).hexdigest()
    def _ready(self):
        if not self._started:raise ProjectAuthoringError("project_not_started")
