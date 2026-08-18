"""Adaptive native-authority binding for Level 3 production BIM."""
from __future__ import annotations
from dataclasses import dataclass,field
from importlib import import_module
from inspect import isclass,signature
from pathlib import Path
from typing import Any
import json
@dataclass(slots=True)
class NativeBinding:
    """Describe one discovered native authority and its runtime compatibility."""
    domain:str; module:str; symbol:str; path:str; score:int; importable:bool=False; resolved:bool=False; compatible_operations:list[str]=field(default_factory=list); error:str|None=None
class NativeAuthorityRegistry:
    """Resolve 001A discovery candidates without assuming undocumented APIs."""
    REQUIRED_DOMAINS=("levels","grids","views","documentation")
    OPERATION_ALIASES={"levels":("create_level","add_level","new_level","create_storey","add_storey"),"grids":("create_grid","add_grid","new_grid","create_axis","add_axis"),"views":("create_view","add_view","new_view","create_plan_view","create_section","create_elevation"),"documentation":("create_sheet","add_sheet","new_sheet","place_view","place_view_on_sheet")}
    def __init__(self,discovery_path:Path):
        self.discovery_path=Path(discovery_path); self.discovery=json.loads(self.discovery_path.read_text(encoding="utf-8-sig")); self.bindings={}; self._objects={}
    def resolve(self):
        """Resolve the best safe candidate for each required domain."""
        amap=self.discovery.get("authority_map",{}); self.bindings.clear(); self._objects.clear()
        for d in self.REQUIRED_DOMAINS:self.bindings[d]=self._resolve_domain(d,amap.get(d,[]))
        return dict(self.bindings)
    def report(self):
        """Return a JSON-compatible compatibility report."""
        if not self.bindings:self.resolve()
        return {"schema":"aias.l3.production-bim.native-binding.v1","bindings":{d:{"module":b.module,"symbol":b.symbol,"path":b.path,"score":b.score,"importable":b.importable,"resolved":b.resolved,"compatible_operations":list(b.compatible_operations),"error":b.error} for d,b in self.bindings.items()},"native_domains_ready":[d for d,b in self.bindings.items() if b.resolved and b.compatible_operations],"fallback_domains":[d for d,b in self.bindings.items() if not(b.resolved and b.compatible_operations)]}
    def _resolve_domain(self,domain,rows):
        last="no_candidate"
        for row in rows:
            b=NativeBinding(domain,row["module"],row["symbol"],row["path"],int(row.get("score",0)))
            try:m=import_module(b.module); b.importable=True; target=getattr(m,b.symbol)
            except Exception as e:last=f"{type(e).__name__}: {e}"; continue
            obj=self._safe_object(target)
            if obj is None:last="symbol_not_safely_instantiable"; continue
            b.resolved=True; b.compatible_operations=[n for n in self.OPERATION_ALIASES.get(domain,()) if callable(getattr(obj,n,None))]; self._objects[domain]=obj; return b
        return NativeBinding(domain,"","","",0,error=last)
    @staticmethod
    def _safe_object(target:Any):
        """Instantiate only no-required-argument classes; pass through module-level objects."""
        if not isclass(target): return target
        try:sig=signature(target)
        except Exception:return None
        req=[p for p in sig.parameters.values() if p.default is p.empty and p.kind in (p.POSITIONAL_ONLY,p.POSITIONAL_OR_KEYWORD,p.KEYWORD_ONLY)]
        if req:return None
        try:return target()
        except Exception:return None
