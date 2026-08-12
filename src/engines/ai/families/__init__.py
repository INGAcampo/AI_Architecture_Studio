from dataclasses import dataclass,field
from typing import Any
@dataclass(frozen=True,slots=True)
class FamilyParameter:
    parameter_id:str
    default:Any=None
    is_type_parameter:bool=True
@dataclass(frozen=True,slots=True)
class FamilyType:
    type_id:str
    values:dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True,slots=True)
class FamilyDefinition:
    family_id:str
    parameters:tuple[FamilyParameter,...]
    types:tuple[FamilyType,...]
class FamilyInstance:
    def __init__(self,instance_id,family,family_type,instance_values=None):
        self.instance_id=instance_id;self.family=family;self.family_type=family_type;self.instance_values=dict(instance_values or {})
    def value(self,key):
        if key in self.instance_values:return self.instance_values[key]
        if key in self.family_type.values:return self.family_type.values[key]
        for p in self.family.parameters:
            if p.parameter_id==key:return p.default
        raise KeyError(key)
