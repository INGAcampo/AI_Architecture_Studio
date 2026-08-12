from dataclasses import dataclass
from copy import deepcopy

@dataclass(frozen=True, slots=True)
class EditResult:
    committed: bool
    changed_ids: tuple[str, ...]
    error: str | None = None

class ArchitecturalEditingAPI:
    def __init__(self):
        self._objects = {}

    def add(self, object_id, obj):
        self._objects[object_id] = obj
        return obj

    def get(self, object_id):
        return self._objects[object_id]

    def transaction(self, operations):
        snapshot = deepcopy(self._objects)
        changed = []
        try:
            for operation in operations:
                object_id, new_object = operation(self)
                self._objects[object_id] = new_object
                changed.append(object_id)
        except Exception as exc:
            self._objects = snapshot
            return EditResult(False, (), str(exc))
        return EditResult(True, tuple(changed))

    def delete(self, object_id):
        return self._objects.pop(object_id)

    def all_ids(self):
        return tuple(sorted(self._objects))
