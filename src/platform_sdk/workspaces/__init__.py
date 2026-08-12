from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class WorkspaceDefinition:
    workspace_id:str; name:str; panels:tuple[str,...]=(); commands:tuple[str,...]=()
class WorkspaceManager:
    def __init__(self): self._items={}; self._active=None
    def register(self,w,replace=False):
        if w.workspace_id in self._items and not replace: raise ValueError("Workspace duplicado")
        self._items[w.workspace_id]=w
        if self._active is None:self._active=w.workspace_id
        return w
    def activate(self,wid): self._active=wid; return self._items[wid]
    @property
    def active(self): return None if self._active is None else self._items[self._active]
    def all(self): return tuple(self._items[k] for k in sorted(self._items))
