from dataclasses import dataclass,field
from enum import Enum
from typing import Any,Mapping
class RelationshipType(str,Enum):
 CONTAINS="contains";HOSTS="hosts";SUPPORTS="supports";DEPENDS_ON="depends_on";CONNECTS_TO="connects_to";BELONGS_TO="belongs_to";REFERENCES="references";CUSTOM="custom"
class RelationshipDirection(str,Enum):
 DIRECTED="directed";BIDIRECTIONAL="bidirectional"
@dataclass(frozen=True,slots=True)
class ObjectRelationship:
 relationship_id:str;source_id:str;target_id:str;relationship_type:RelationshipType;direction:RelationshipDirection=RelationshipDirection.DIRECTED;priority:int=0;metadata:Mapping[str,Any]=field(default_factory=dict)
 def __post_init__(self):
  if not self.relationship_id.strip() or not self.source_id.strip() or not self.target_id.strip(): raise ValueError("Campos obligatorios")
  if self.source_id==self.target_id: raise ValueError("No se permiten autorrelaciones")
