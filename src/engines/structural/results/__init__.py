from dataclasses import dataclass
from enum import Enum

class ResultKind(str, Enum):
    DISPLACEMENT="displacement"
    REACTION="reaction"
    MEMBER_FORCE="member_force"
    STRESS="stress"
    MODE_SHAPE="mode_shape"

@dataclass(frozen=True, slots=True)
class StructuralResult:
    result_id: str
    case_id: str
    object_id: str
    kind: ResultKind
    values: tuple[float, ...]
    def __post_init__(self):
        if not self.result_id.strip() or not self.case_id.strip() or not self.object_id.strip():
            raise ValueError("Identificadores obligatorios")
        if not self.values:
            raise ValueError("values no puede estar vacío")

class StructuralResultStore:
    def __init__(self):
        self._items = {}
    def add(self, result):
        if result.result_id in self._items:
            raise KeyError(result.result_id)
        self._items[result.result_id] = result
        return result
    def for_case(self, case_id):
        return tuple(r for r in self._items.values() if r.case_id == case_id)
    def for_object(self, object_id):
        return tuple(r for r in self._items.values() if r.object_id == object_id)
