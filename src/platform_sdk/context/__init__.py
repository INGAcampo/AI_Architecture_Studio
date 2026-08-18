from dataclasses import dataclass
from platform_sdk.services import ServiceRegistry
from platform_sdk.events import GlobalEventBus
from platform_sdk.commands import CommandBus
from platform_sdk.workspaces import WorkspaceManager
from platform_sdk.documents import DocumentManager
from platform_sdk.plugins import PluginManager
@dataclass(slots=True)
class PlatformContext:
    services:ServiceRegistry; events:GlobalEventBus; commands:CommandBus; workspaces:WorkspaceManager; documents:DocumentManager; plugins:PluginManager
    @classmethod
    def create_default(cls): return cls(ServiceRegistry(),GlobalEventBus(),CommandBus(),WorkspaceManager(),DocumentManager(),PluginManager())
