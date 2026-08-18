"""Progressive native integration for levels, grids, views and sheets."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .authority_binding import NativeAuthorityRegistry
from .service import NativeProjectAuthoringService
class NativeProjectIntegrationService(NativeProjectAuthoringService):
    """Mirror canonical 001B authoring into compatible native authorities."""
    def __init__(self,project_name:str,*,discovery_path:Path,project_number:str="",description:str="",units:str="metric",**ui:Any):
        super().__init__(project_name,project_number=project_number,description=description,units=units,**ui); self.authorities=NativeAuthorityRegistry(discovery_path); self.authorities.resolve(); self.native_results={d:[] for d in ("levels","grids","views","documentation")}
    def add_level(self,name,elevation,**properties):
        """Create canonical level and mirror to a compatible native authority."""
        x=super().add_level(name,elevation,**properties); self._mirror("levels",[("create_level",(name,float(elevation)),properties),("add_level",(name,float(elevation)),properties),("new_level",(name,float(elevation)),properties),("create_storey",(name,float(elevation)),properties),("add_storey",(name,float(elevation)),properties)]); return x
    def add_grid(self,name,start,end,**properties):
        """Create canonical grid and mirror to a compatible native authority."""
        x=super().add_grid(name,start,end,**properties); self._mirror("grids",[("create_grid",(name,start,end),properties),("add_grid",(name,start,end),properties),("new_grid",(name,start,end),properties),("create_axis",(name,start,end),properties),("add_axis",(name,start,end),properties)]); return x
    def add_view(self,name,view_type,*,level_id=None,**properties):
        """Create canonical view and mirror to a compatible native authority."""
        x=super().add_view(name,view_type,level_id=level_id,**properties); kw={"level_id":level_id,**properties}; self._mirror("views",[("create_view",(name,view_type),kw),("add_view",(name,view_type),kw),("new_view",(name,view_type),kw)]); return x
    def add_sheet(self,number,name,view_ids=None):
        """Create canonical sheet and mirror to a compatible native documentation authority."""
        x=super().add_sheet(number,name,view_ids); self._mirror("documentation",[("create_sheet",(number,name),{}),("add_sheet",(number,name),{}),("new_sheet",(number,name),{})]); return x
    def place_view_on_sheet(self,sheet_id,view_id):
        """Place a canonical view and mirror placement when supported."""
        super().place_view_on_sheet(sheet_id,view_id); self._mirror("documentation",[("place_view_on_sheet",(sheet_id,view_id),{}),("place_view",(sheet_id,view_id),{})])
    def native_binding_report(self):
        """Return compatibility and mirror counts."""
        r=self.authorities.report(); r["mirrored_operations"]={d:len(v) for d,v in self.native_results.items()}; return r
    def _mirror(self,domain,attempts):
        obj=self.authorities._objects.get(domain)
        if obj is None:return
        for name,args,kwargs in attempts:
            f=getattr(obj,name,None)
            if not callable(f):continue
            try:r=f(*args,**kwargs)
            except Exception:continue
            self.native_results[domain].append(r); return
