from abc import ABC, abstractmethod

class OptimizerPlugin(ABC):
    plugin_id: str

    @abstractmethod
    def optimize(self, kernel, population):
        raise NotImplementedError

class OptimizerPluginRegistry:
    def __init__(self):
        self._plugins = {}

    def register(self, plugin):
        if plugin.plugin_id in self._plugins:
            raise ValueError(f"Plugin duplicado: {plugin.plugin_id}")
        self._plugins[plugin.plugin_id] = plugin

    def get(self, plugin_id):
        return self._plugins[plugin_id]

    def all(self):
        return tuple(self._plugins.values())
