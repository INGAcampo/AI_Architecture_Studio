"""
AI Architecture Studio
Kernel - Object Registry

Foundation 1.7
"""


class ObjectRegistry:
    def __init__(self):
        self._objects = {}

    def register(self, obj):
        self._objects[obj.id] = obj

    def unregister(self, obj_id):
        if obj_id in self._objects:
            del self._objects[obj_id]

    def get(self, obj_id):
        return self._objects.get(obj_id)

    def all(self):
        return list(self._objects.values())

    def count(self):
        return len(self._objects)