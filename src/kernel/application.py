"""
AI Architecture Studio
Kernel - Application

Foundation 1.7
"""

from kernel.version_manager import VersionManager
from kernel.event_bus import EventBus
from kernel.service_locator import ServiceLocator
from kernel.object_registry import ObjectRegistry
from kernel.plugin_manager import PluginManager


class AIASKernel:
    def __init__(self):
        self.version = VersionManager()

        self.event_bus = EventBus()
        self.services = ServiceLocator()
        self.registry = ObjectRegistry()
        self.plugins = PluginManager()

        self.services.register("event_bus", self.event_bus)
        self.services.register("object_registry", self.registry)
        self.services.register("plugin_manager", self.plugins)

    def info(self):
        return {
            "version": self.version.full_version(),
            "services": list(self.services._services.keys()),
            "plugins": self.plugins.count(),
            "objects": self.registry.count(),
        }