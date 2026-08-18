from aec_orchestrator_journal.journal import ReconciliationJournal

def test_journal_sequence_is_monotonic():
    j=ReconciliationJournal()
    a=j.record("OP1","STARTED")
    b=j.record("OP1","COMPLETED")
    assert (a.sequence,b.sequence)==(1,2)
    assert j.has_completed("OP1") is True

def test_duplicate_completion_is_rejected():
    j=ReconciliationJournal()
    j.record("OP1","COMPLETED")
    try:
        j.record("OP1","COMPLETED")
    except ValueError:
        return
    assert False
