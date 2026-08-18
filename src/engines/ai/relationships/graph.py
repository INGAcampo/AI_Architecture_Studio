from collections import defaultdict,deque
from .model import ObjectRelationship,RelationshipType
class RelationshipIntegrityError(ValueError): pass
class RelationshipCycleError(RelationshipIntegrityError): pass
class RelationshipGraph:
 _ACYCLIC={RelationshipType.CONTAINS,RelationshipType.HOSTS,RelationshipType.SUPPORTS,RelationshipType.DEPENDS_ON,RelationshipType.BELONGS_TO}
 def __init__(self):
  self._nodes=set();self._rels={};self._out=defaultdict(set);self._in=defaultdict(set)
 def add_relationship(self,r,replace=False):
  if r.relationship_id in self._rels and not replace: raise RelationshipIntegrityError("Relación duplicada")
  old=self._rels.get(r.relationship_id)
  if old:
   self._out[old.source_id].discard(old.relationship_id);self._in[old.target_id].discard(old.relationship_id)
  self._nodes|={r.source_id,r.target_id};self._rels[r.relationship_id]=r;self._out[r.source_id].add(r.relationship_id);self._in[r.target_id].add(r.relationship_id)
  if r.relationship_type in self._ACYCLIC and self.has_cycle(r.relationship_type):
   self.remove_relationship(r.relationship_id);raise RelationshipCycleError("La relación crea un ciclo")
 def remove_relationship(self,rid):
  r=self._rels.pop(rid);self._out[r.source_id].discard(rid);self._in[r.target_id].discard(rid);return r
 def outgoing(self,obj,t=None):
  rs=[self._rels[i] for i in self._out.get(obj,())]
  return tuple(sorted((r for r in rs if t is None or r.relationship_type is t),key=lambda r:(-r.priority,r.relationship_id)))
 def incoming(self,obj,t=None):
  rs=[self._rels[i] for i in self._in.get(obj,())]
  return tuple(sorted((r for r in rs if t is None or r.relationship_type is t),key=lambda r:(-r.priority,r.relationship_id)))
 def relationships(self): return tuple(sorted(self._rels.values(),key=lambda r:(-r.priority,r.relationship_id)))
 def has_cycle(self,t):
  edges=defaultdict(set)
  for r in self._rels.values():
   if r.relationship_type is t: edges[r.source_id].add(r.target_id)
  seen=set();active=set()
  def visit(n):
   if n in active:return True
   if n in seen:return False
   seen.add(n);active.add(n)
   for m in edges.get(n,()):
    if visit(m):return True
   active.remove(n);return False
  return any(visit(n) for n in self._nodes)
 def descendants(self,obj,t):
  seen=set();q=deque([obj])
  while q:
   n=q.popleft()
   for r in self.outgoing(n,t):
    if r.target_id not in seen: seen.add(r.target_id);q.append(r.target_id)
  return tuple(sorted(seen))
 def ancestors(self,obj,t):
  seen=set();q=deque([obj])
  while q:
   n=q.popleft()
   for r in self.incoming(n,t):
    if r.source_id not in seen: seen.add(r.source_id);q.append(r.source_id)
  return tuple(sorted(seen))
 def neighbors(self,obj):
  return tuple(sorted({r.target_id for r in self.outgoing(obj)}|{r.source_id for r in self.incoming(obj)}))
 def __len__(self): return len(self._rels)
