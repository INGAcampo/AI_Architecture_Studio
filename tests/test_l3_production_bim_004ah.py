from aias_l3_production_bim.autocad_production_write_gate import (
    PRODUCTION_APPROVAL_TOKEN,
    ProductionWritePreflight,
    evaluate_production_write_gate,
)


def clean():
    return ProductionWritePreflight(
        exact_document_match=True,
        modelspace_parity=True,
        read_only=False,
        physical_path_present=True,
        undo_mark_supported=True,
        saved_state_known=True,
        baseline_entity_count=4256,
        live_entity_count=4256,
    )


def test_clean_preflight_is_technically_eligible():
    assert clean().technically_eligible is True


def test_no_explicit_approval_never_authorizes():
    d = evaluate_production_write_gate(clean())
    assert d.authorized is False
    assert d.technically_eligible is True
    assert d.production_write_enabled is False
    assert d.scope == "PREFLIGHT_ONLY"


def test_wrong_token_never_authorizes():
    d = evaluate_production_write_gate(
        clean(),
        explicit_user_approval=True,
        approval_token="WRONG",
    )
    assert d.authorized is False
    assert d.production_write_enabled is False


def test_exact_token_plus_explicit_approval_authorizes_contract_only():
    d = evaluate_production_write_gate(
        clean(),
        explicit_user_approval=True,
        approval_token=PRODUCTION_APPROVAL_TOKEN,
    )
    assert d.authorized is True
    assert d.scope == "CONTROLLED_ONE_ENTITY_NO_SAVE_TRANSACTION"
    assert d.production_write_enabled is False


def test_read_only_blocks():
    p = ProductionWritePreflight(
        exact_document_match=True,
        modelspace_parity=True,
        read_only=True,
        physical_path_present=True,
        undo_mark_supported=True,
        saved_state_known=True,
        baseline_entity_count=4256,
        live_entity_count=4256,
    )
    d = evaluate_production_write_gate(
        p,
        explicit_user_approval=True,
        approval_token=PRODUCTION_APPROVAL_TOKEN,
    )
    assert d.authorized is False
    assert d.technically_eligible is False


def test_parity_mismatch_blocks():
    p = ProductionWritePreflight(
        exact_document_match=True,
        modelspace_parity=False,
        read_only=False,
        physical_path_present=True,
        undo_mark_supported=True,
        saved_state_known=True,
        baseline_entity_count=4256,
        live_entity_count=4257,
    )
    assert evaluate_production_write_gate(p).authorized is False


def test_missing_undo_support_blocks():
    p = ProductionWritePreflight(
        exact_document_match=True,
        modelspace_parity=True,
        read_only=False,
        physical_path_present=True,
        undo_mark_supported=False,
        saved_state_known=True,
        baseline_entity_count=4256,
        live_entity_count=4256,
    )
    assert p.technically_eligible is False
