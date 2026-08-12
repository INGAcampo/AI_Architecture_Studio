from dataclasses import dataclass
from enum import Enum

class LoadCategory(str,Enum):
    DEAD="dead";LIVE="live";ROOF="roof";WIND="wind";SEISMIC="seismic";SNOW="snow";TEMPERATURE="temperature";CONSTRUCTION="construction"

@dataclass(frozen=True,slots=True)
class LoadCase:
    case_id:str
    name:str
    category:LoadCategory
    self_weight_multiplier:float=0.0
    metadata:dict=None

class LoadCaseEngine:
    def __init__(self): self._cases={}
    def add(self,case):
        if case.case_id in self._cases: raise ValueError("Caso duplicado")
        self._cases[case.case_id]=case;return case
    def get(self,case_id): return self._cases[case_id]
    def by_category(self,category):
        return tuple(sorted((c for c in self._cases.values() if c.category is category),key=lambda c:c.case_id))
