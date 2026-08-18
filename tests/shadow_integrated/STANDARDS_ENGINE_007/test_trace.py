from standards_engine_trace.trace import DecisionTrace,append_trace_event

def test_trace_sequence_is_monotonic():
    t=DecisionTrace()
    t=append_trace_event(t,"SOURCE",True,"accepted")
    t=append_trace_event(t,"PROVENANCE",True,"accepted")
    t=append_trace_event(t,"APPLICABILITY",False,"not_applicable")
    assert tuple(e.sequence for e in t.events)==(1,2,3)
    assert t.events[-1].accepted is False

def test_blank_stage_fails_closed():
    try:
        append_trace_event(DecisionTrace(),"",True,"accepted")
    except ValueError:
        return
    assert False
