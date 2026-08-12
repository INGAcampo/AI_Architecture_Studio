"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True, slots=True)
class PluginDescriptor:
    """Execute the public PluginDescriptor operation for the Omega application core and shared runtime services using explicit caller inputs."""
    plugin_id: str
    name: str
    version: str
    factory: Callable[..., Any]

class PluginRegistry:
    """Execute the public PluginRegistry operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._plugins: dict[str, PluginDescriptor] = {}

    def register(self, descriptor: PluginDescriptor) -> None:
        """Add register to the Omega application core and shared runtime services while enforcing identity constraints."""
        if descriptor.plugin_id in self._plugins:
            raise ValueError(descriptor.plugin_id)
        self._plugins[descriptor.plugin_id] = descriptor

    def create(self, plugin_id: str, *args, **kwargs):
        """Build the create required by the Omega application core and shared runtime services from explicit inputs."""
        return self._plugins[plugin_id].factory(*args, **kwargs)

    def all(self) -> tuple[PluginDescriptor, ...]:
        """Execute the public PluginRegistry.all operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return tuple(self._plugins.values())
