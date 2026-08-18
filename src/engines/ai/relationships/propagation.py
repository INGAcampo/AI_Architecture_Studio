from dataclasses import dataclass,field
from typing import Any
from .query import RelationshipQuery
@dataclass(frozen=True,slots=True)
class PropagationEvent:
 source_id:str;event_type:str;payload:dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True,slots=True)
class PropagationReport:
 source_id:str;event_type:str;affected_objects:tuple[str,...];ordered_actions:tuple[tuple[str,str],...];errors:tuple[str,...]
 @property
 def success(self): return not self.errors
class RelationshipPropagationEngine:
 def __init__(self,graph): self.query=RelationshipQuery(graph)
 def propagate(self,event):
  mapping={"move":"reposition","resize":"regenerate","delete":"validate_or_remove","property_changed":"refresh_properties","geometry_changed":"regenerate_geometry"}
  affected=self.query.impact_of(event.source_id);action=mapping.get(event.event_type)
  errors=() if action else tuple(f"No existe acción para {event.event_type} sobre {o}" for o in affected)
  actions=tuple((o,action) for o in affected) if action else ()
  return PropagationReport(event.source_id,event.event_type,affected,actions,errors)
