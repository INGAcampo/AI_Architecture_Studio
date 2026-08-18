from dataclasses import dataclass
from enum import Enum
class CoordinationStatus(str,Enum):
    CLEAN="clean";WARNING="warning";CONFLICT="conflict"
@dataclass(frozen=True,slots=True)
class InfrastructureAsset:
    asset_id:str
    discipline:str
    revision:int
class InfrastructureBimCoordinator:
    def compare(self,a,b):
        if a.asset_id!=b.asset_id:return CoordinationStatus.CONFLICT
        if a.revision==b.revision:return CoordinationStatus.CLEAN
        return CoordinationStatus.WARNING
    def latest(self,assets): return max(assets,key=lambda x:x.revision)
