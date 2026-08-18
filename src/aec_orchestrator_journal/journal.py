from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class JournalEntry:
    sequence:int
    operation_id:str
    state:str

class ReconciliationJournal:
    def __init__(self):
        self._entries=[]
        self._completed=set()

    def record(self,operation_id:str,state:str)->JournalEntry:
        if not operation_id.strip() or not state.strip():
            raise ValueError("journal fields must not be empty")

        if state=="COMPLETED" and operation_id in self._completed:
            raise ValueError("duplicate completed operation")

        entry=JournalEntry(len(self._entries)+1,operation_id,state)
        self._entries.append(entry)

        if state=="COMPLETED":
            self._completed.add(operation_id)

        return entry

    def has_completed(self,operation_id:str)->bool:
        return operation_id in self._completed

    @property
    def entries(self):
        return tuple(self._entries)
