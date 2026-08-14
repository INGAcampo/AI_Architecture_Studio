from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DecisionTraceEvent:
    sequence:int
    stage:str
    accepted:bool
    reason:str

@dataclass(frozen=True)
class DecisionTrace:
    events:tuple[DecisionTraceEvent,...]=()

def append_trace_event(trace:DecisionTrace,stage:str,accepted:bool,reason:str)->DecisionTrace:
    if not stage.strip():
        raise ValueError("stage must not be empty")
    if not reason.strip():
        raise ValueError("reason must not be empty")

    event=DecisionTraceEvent(
        len(trace.events)+1,
        stage,
        bool(accepted),
        reason,
    )
    return DecisionTrace(trace.events+(event,))
