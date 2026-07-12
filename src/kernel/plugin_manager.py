"""
AI Architecture Studio
Kernel - Plugin Manager

Foundation 1.7
"""


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, name, plugin):
        self.plugins[name] = plugin

    def unregister_plugin(self, name):
        if name in self.plugins:
            del self.plugins[name]

    def get_plugin(self, name):
        return self.plugins.get(name)

    def all_plugins(self):
        return self.plugins

    def count(self):
        return len(self.plugins)