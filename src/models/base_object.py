"""
AI Architecture Studio
Base Object

Foundation 1.6
"""

import uuid


class BaseObject:
    def __init__(self, name, object_type):
        self.id = str(uuid.uuid4())
        self.name = name
        self.object_type = object_type
        self.geometry = None
        self.properties = {}

    def set_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key, default=None):
        return self.properties.get(key, default)

    def info(self):
        return {
            "ID": self.id,
            "Nombre": self.name,
            "Tipo": self.object_type,
            "Propiedades": self.properties,
        }