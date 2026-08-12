from dataclasses import dataclass
from platform_sdk.bootstrap import PlatformBootstrap
@dataclass(frozen=True,slots=True)
class PlatformStatus:
    ready:bool; services:tuple[str,...]; workspaces:tuple[str,...]; active_workspace:str|None
class AIASPlatformSDK:
    VERSION="1.0"
    def __init__(self): self._boot=None
    def start(self): self._boot=PlatformBootstrap().build(); return self.status()
    def status(self):
        if self._boot is None:return PlatformStatus(False,(),(),None)
        c=self._boot.context
        return PlatformStatus(True,c.services.ids(),tuple(w.workspace_id for w in c.workspaces.all()),c.workspaces.active.workspace_id)
