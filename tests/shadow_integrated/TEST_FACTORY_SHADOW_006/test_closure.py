from shadow_test_factory_closure.closure import audit_dependency_closure

def test_dependency_closure_passes_complete_chain():
    result=audit_dependency_closure(
        (
            {"megablock":"A","dependency":""},
            {"megablock":"B","dependency":"A"},
            {"megablock":"C","dependency":"B"},
        )
    )
    assert result.passed is True

def test_missing_dependency_is_detected():
    result=audit_dependency_closure(
        (
            {"megablock":"B","dependency":"A"},
        )
    )
    assert result.passed is False
    assert result.missing_dependencies==("B->A",)

def test_self_dependency_is_detected():
    result=audit_dependency_closure(
        (
            {"megablock":"A","dependency":"A"},
        )
    )
    assert result.passed is False
    assert result.self_dependencies==("A",)
