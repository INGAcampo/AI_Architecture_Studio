class SteelProfileRepository:
 def __init__(self): self._items={}
 def register(self,p,replace=False):
  if p.profile_id in self._items and not replace: raise ValueError('Perfil duplicado')
  self._items[p.profile_id]=p;return p
 def get(self,pid): return self._items[pid]
 def all(self): return tuple(self._items[k] for k in sorted(self._items))
 def by_family(self,f): return tuple(p for p in self.all() if p.family is f)
 def search(self,t):
  q=t.casefold();return tuple(p for p in self.all() if q in p.profile_id.casefold() or q in p.designation.casefold())
class SteelMaterialRepository:
 def __init__(self): self._items={}
 def register(self,m,replace=False):
  if m.material_id in self._items and not replace: raise ValueError('Material duplicado')
  self._items[m.material_id]=m;return m
 def get(self,mid): return self._items[mid]
 def all(self): return tuple(self._items[k] for k in sorted(self._items))
