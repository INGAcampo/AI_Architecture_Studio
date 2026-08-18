from dataclasses import dataclass
from copy import deepcopy
@dataclass(frozen=True,slots=True)
class StructuralTransactionResult: committed:bool; changed_ids:tuple[str,...]; error:str|None=None
class StructuralTransactionManager:
 def __init__(self): self.objects={}
 def add(self,i,o): self.objects[i]=o
 def get(self,i): return self.objects[i]
 def commit(self,ops,validators=()):
  snap=deepcopy(self.objects); changed=[]
  try:
   for op in ops:
    i,o=op(self); self.objects[i]=o; changed.append(i)
   for val in validators:
    e=val(self.objects)
    if e: raise ValueError(e)
  except Exception as exc:
   self.objects=snap; return StructuralTransactionResult(False,(),str(exc))
  return StructuralTransactionResult(True,tuple(changed))
