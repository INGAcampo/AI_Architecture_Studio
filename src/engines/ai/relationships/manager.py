from .graph import RelationshipGraph
from .model import ObjectRelationship,RelationshipDirection,RelationshipType
class RelationshipManager:
 def __init__(self,graph=None): self.graph=graph or RelationshipGraph()
 def connect(self,rid,source,target,t,direction=RelationshipDirection.DIRECTED,priority=0,metadata=None,replace=False):
  r=ObjectRelationship(rid,source,target,t,direction,priority,metadata or {});self.graph.add_relationship(r,replace=replace);return r
 def disconnect(self,rid): return self.graph.remove_relationship(rid)
 def parent(self,obj,t=RelationshipType.CONTAINS):
  r=self.graph.incoming(obj,t);return r[0].source_id if r else None
 def children(self,obj,t=RelationshipType.CONTAINS): return tuple(r.target_id for r in self.graph.outgoing(obj,t))
 def dependencies(self,obj): return tuple(r.target_id for r in self.graph.outgoing(obj,RelationshipType.DEPENDS_ON))
 def dependents(self,obj): return tuple(r.source_id for r in self.graph.incoming(obj,RelationshipType.DEPENDS_ON))
 def connections(self,obj): return self.graph.neighbors(obj)
