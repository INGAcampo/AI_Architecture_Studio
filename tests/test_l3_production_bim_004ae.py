from aias_l3_production_bim.autocad_write_gate import (
    SANDBOX_APPROVAL_TOKEN,
    evaluate_write_gate,
)


def test_gate_rejects_missing_token():
    d = evaluate_write_gate(token=None, temporary_document=True)
    assert d.approved is False
    assert d.production_write_enabled is False


def test_gate_rejects_wrong_token():
    d = evaluate_write_gate(token="WRONG", temporary_document=True)
    assert d.approved is False


def test_gate_rejects_real_document_even_with_token():
    d = evaluate_write_gate(
        token=SANDBOX_APPROVAL_TOKEN,
        temporary_document=False,
    )
    assert d.approved is False
    assert d.production_write_enabled is False


def test_gate_allows_exact_temp_scope_only():
    d = evaluate_write_gate(
        token=SANDBOX_APPROVAL_TOKEN,
        temporary_document=True,
    )
    assert d.approved is True
    assert d.scope == "TEMPORARY_UNSAVED_DOCUMENT_ONE_LINE"
    assert d.production_write_enabled is False
