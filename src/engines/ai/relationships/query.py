from .model import RelationshipType
class RelationshipQuery:
 def __init__(self,graph): self.graph=graph
 def children_of(self,obj,t=RelationshipType.CONTAINS): return tuple(r.target_id for r in self.graph.outgoing(obj,t))
 def parents_of(self,obj,t=RelationshipType.CONTAINS): return tuple(r.source_id for r in self.graph.incoming(obj,t))
 def descendants_of(self,obj,t): return self.graph.descendants(obj,t)
 def ancestors_of(self,obj,t): return self.graph.ancestors(obj,t)
 def impact_of(self,obj):
  x=set()
  for t in (RelationshipType.CONTAINS,RelationshipType.HOSTS,RelationshipType.SUPPORTS): x.update(self.graph.descendants(obj,t))
  x.update(r.source_id for r in self.graph.incoming(obj,RelationshipType.DEPENDS_ON))
  return tuple(sorted(x))
