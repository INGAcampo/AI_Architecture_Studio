from dataclasses import dataclass
from enum import Enum

class AnalysisCaseKind(str, Enum):
    STATIC="static"
    MODAL="modal"
    BUCKLING="buckling"
    RESPONSE_SPECTRUM="response_spectrum"

@dataclass(frozen=True, slots=True)
class AnalysisCase:
    case_id: str
    name: str
    kind: AnalysisCaseKind
    load_combination_id: str | None = None
    active: bool = True
    def __post_init__(self):
        if not self.case_id.strip() or not self.name.strip():
            raise ValueError("Identificadores obligatorios")

class AnalysisCaseManager:
    def __init__(self):
        self._items = {}
    def add(self, case):
        if case.case_id in self._items:
            raise KeyError(case.case_id)
        self._items[case.case_id] = case
        return case
    def get(self, case_id):
        return self._items[case_id]
    def active_cases(self):
        return tuple(item for item in self._items.values() if item.active)
