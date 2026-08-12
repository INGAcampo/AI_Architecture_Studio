from dataclasses import dataclass
from enum import Enum
class SyncAction(str,Enum): CREATE="create";UPDATE="update";DELETE="delete";NOOP="noop"
@dataclass(frozen=True,slots=True)
class SyncRecord:
    object_id:str;source_revision:int;target_revision:int;action:SyncAction
class StructuralModelSynchronizer:
    def decide(self,object_id,source_revision,target_revision,exists_source=True,exists_target=True):
        if exists_source and not exists_target:return SyncRecord(object_id,source_revision,target_revision,SyncAction.CREATE)
        if not exists_source and exists_target:return SyncRecord(object_id,source_revision,target_revision,SyncAction.DELETE)
        if source_revision>target_revision:return SyncRecord(object_id,source_revision,target_revision,SyncAction.UPDATE)
        return SyncRecord(object_id,source_revision,target_revision,SyncAction.NOOP)
