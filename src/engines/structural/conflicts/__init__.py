from dataclasses import dataclass
from enum import Enum
class ConflictResolution(str,Enum): SOURCE_WINS="source_wins";TARGET_WINS="target_wins";MERGED="merged";MANUAL="manual"
@dataclass(frozen=True,slots=True)
class ChangeSet:
    object_id:str;source_values:dict;target_values:dict
class ConflictResolver:
    def conflicts(self,c):
        keys=set(c.source_values)|set(c.target_values);return tuple(sorted(k for k in keys if c.source_values.get(k)!=c.target_values.get(k)))
    def resolve(self,c,strategy):
        if strategy is ConflictResolution.SOURCE_WINS:return dict(c.source_values)
        if strategy is ConflictResolution.TARGET_WINS:return dict(c.target_values)
        if strategy is ConflictResolution.MERGED:
            m=dict(c.target_values);m.update(c.source_values);return m
        raise ValueError("Resolución manual requerida")
