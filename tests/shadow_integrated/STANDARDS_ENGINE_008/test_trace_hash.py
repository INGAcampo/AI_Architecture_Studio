from standards_engine_trace.trace import DecisionTrace,append_trace_event
from standards_engine_trace_hash.hashing import decision_trace_sha256

def test_trace_hash_is_deterministic():
    t=DecisionTrace()
    t=append_trace_event(t,"SOURCE",True,"accepted")
    t=append_trace_event(t,"PROVENANCE",True,"accepted")
    assert decision_trace_sha256(t)==decision_trace_sha256(t)
    assert len(decision_trace_sha256(t))==64

def test_trace_change_changes_hash():
    a=append_trace_event(DecisionTrace(),"SOURCE",True,"accepted")
    b=append_trace_event(DecisionTrace(),"SOURCE",False,"rejected")
    assert decision_trace_sha256(a)!=decision_trace_sha256(b)
