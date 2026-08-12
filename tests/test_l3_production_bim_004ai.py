from aias_l3_production_bim.autocad_production_write_gate import (
    PRODUCTION_APPROVAL_TOKEN,
    ProductionWritePreflight,
)
from aias_l3_production_bim.autocad_controlled_production_exercise import (
    ControlledProductionExerciseApproval,
    validate_004ai_approval,
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


def approval(**kwargs):
    data = dict(
        user_approved=True,
        approval_token=PRODUCTION_APPROVAL_TOKEN,
        one_entity_only=True,
        rollback_required=True,
        save_forbidden=True,
        send_command_forbidden=True,
    )
    data.update(kwargs)
    return ControlledProductionExerciseApproval(**data)


def test_exact_contract_authorizes():
    assert validate_004ai_approval(clean(), approval()) is True


def test_missing_user_approval_blocks():
    assert validate_004ai_approval(clean(), approval(user_approved=False)) is False


def test_wrong_token_blocks():
    assert validate_004ai_approval(clean(), approval(approval_token="WRONG")) is False


def test_more_than_one_entity_scope_blocks():
    assert validate_004ai_approval(clean(), approval(one_entity_only=False)) is False


def test_optional_rollback_blocks():
    assert validate_004ai_approval(clean(), approval(rollback_required=False)) is False


def test_save_permission_blocks():
    assert validate_004ai_approval(clean(), approval(save_forbidden=False)) is False


def test_sendcommand_permission_blocks():
    assert validate_004ai_approval(clean(), approval(send_command_forbidden=False)) is False


def test_dirty_preflight_blocks():
    dirty = ProductionWritePreflight(
        exact_document_match=True,
        modelspace_parity=False,
        read_only=False,
        physical_path_present=True,
        undo_mark_supported=True,
        saved_state_known=True,
        baseline_entity_count=4256,
        live_entity_count=4257,
    )
    assert validate_004ai_approval(dirty, approval()) is False
