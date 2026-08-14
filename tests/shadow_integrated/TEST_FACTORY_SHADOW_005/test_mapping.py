from shadow_test_factory_reconcile_map.mapping import classify_canonical_overlap

def test_missing_canonical_target_is_additive():
    r=classify_canonical_overlap("shadow/a.py","src/a.py",False)
    assert r.classification=="ADDITIVE_CANDIDATE"

def test_existing_canonical_target_requires_reconciliation():
    r=classify_canonical_overlap("shadow/a.py","src/a.py",True)
    assert r.classification=="REQUIRES_CONTENT_RECONCILIATION"
