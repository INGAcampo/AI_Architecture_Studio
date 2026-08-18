from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PluginManifest:
    plugin_id:str; name:str; version:str; required_services:tuple[str,...]=()
class PluginManager:
    def __init__(self): self._items={}; self._active=set()
    def register(self,p): self._items[p.manifest.plugin_id]=p; return p
    def activate(self,pid,context):
        p=self._items[pid]
        missing=[s for s in p.manifest.required_services if not context.services.contains(s)]
        if missing: raise RuntimeError("Servicios faltantes")
        p.activate(context); self._active.add(pid); return p
    def is_active(self,pid): return pid in self._active
