from dataclasses import dataclass,field
from enum import Enum
class DocumentKind(str,Enum): MODEL="model";DRAWING="drawing";ANALYSIS="analysis";REPORT="report"
@dataclass(slots=True)
class PlatformDocument:
    document_id:str; name:str; kind:DocumentKind; content:object=None; revision:int=0; dirty:bool=False; metadata:dict=field(default_factory=dict)
class DocumentManager:
    def __init__(self): self._items={}; self._active=None
    def create(self,d): self._items[d.document_id]=d; self._active=d.document_id; return d
    def get(self,did): return self._items[did]
    def mark_changed(self,did):
        d=self.get(did); d.revision+=1; d.dirty=True; return d
    def mark_saved(self,did): d=self.get(did); d.dirty=False; return d
    @property
    def active(self): return None if self._active is None else self.get(self._active)
