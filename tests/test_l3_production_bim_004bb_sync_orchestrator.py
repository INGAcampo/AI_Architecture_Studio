import pytest

from aias_l3_production_bim.autocad_persistent_sync_state import (
    AIASSyncRecord,
)
from aias_l3_production_bim.autocad_sync_orchestrator import (
    OrchestratorAction,
    build_dry_run_plan,
    plan_record,
    plan_to_payload,
)


DOC = "abc123"


def rec(handle="A1", base="b", aias="b", acad="b"):
    h = handle.upper()
    return AIASSyncRecord(
        document_key=DOC,
        aias_id=f"autocad:{DOC}:{h}",
        autocad_handle=h,
        baseline_fingerprint=base,
        aias_fingerprint=aias,
        autocad_fingerprint=acad,
    )


@pytest.mark.parametrize(
    "record,expected",
    [
        (rec(), OrchestratorAction.NOOP),
        (rec(aias="changed"), OrchestratorAction.BLOCKED_PUSH_TO_AUTOCAD),
        (rec(acad="changed"), OrchestratorAction.PULL_INTO_AIAS),
        (rec(aias="a", acad="c"), OrchestratorAction.MANUAL_CONFLICT_REVIEW),
        (rec(aias=None, acad="b"), OrchestratorAction.CREATE_AIAS_REPRESENTATION),
        (rec(aias="b", acad=None), OrchestratorAction.REVIEW_MISSING_AUTOCAD_ENTITY),
    ],
)
def test_action_mapping(record, expected):
    item = plan_record(record)
    assert item.orchestrator_action is expected
    assert item.dry_run
    assert not item.autocad_write_allowed
    assert not item.autocad_delete_allowed


def test_aias_changed_requires_manual_review():
    item = plan_record(rec(aias="changed"))
    assert item.requires_manual_review


def test_autocad_changed_pull_is_not_manual_conflict():
    item = plan_record(rec(acad="changed"))
    assert item.orchestrator_action is OrchestratorAction.PULL_INTO_AIAS
    assert not item.requires_manual_review


def test_conflict_requires_manual_review():
    item = plan_record(rec(aias="x", acad="y"))
    assert item.requires_manual_review


def test_missing_autocad_requires_manual_review():
    item = plan_record(rec(acad=None))
    assert item.requires_manual_review


def test_plan_summary_clean():
    plan = build_dry_run_plan(DOC, [rec("A1"), rec("A2")])
    assert plan.action_count == 2
    assert plan.summary()[OrchestratorAction.NOOP.value] == 2
    assert plan.automatic_autocad_write_count == 0
    assert plan.automatic_autocad_delete_count == 0
    assert plan.manual_review_count == 0


def test_plan_mixed_matrix():
    plan = build_dry_run_plan(
        DOC,
        [
            rec("A1"),
            rec("A2", aias="changed"),
            rec("A3", acad="changed"),
            rec("A4", aias="x", acad="y"),
            rec("A5", aias=None, acad="b"),
            rec("A6", acad=None),
        ],
    )
    summary = plan.summary()
    assert summary[OrchestratorAction.NOOP.value] == 1
    assert summary[OrchestratorAction.BLOCKED_PUSH_TO_AUTOCAD.value] == 1
    assert summary[OrchestratorAction.PULL_INTO_AIAS.value] == 1
    assert summary[OrchestratorAction.MANUAL_CONFLICT_REVIEW.value] == 1
    assert summary[OrchestratorAction.CREATE_AIAS_REPRESENTATION.value] == 1
    assert summary[OrchestratorAction.REVIEW_MISSING_AUTOCAD_ENTITY.value] == 1
    assert plan.automatic_autocad_write_count == 0
    assert plan.automatic_autocad_delete_count == 0


def test_duplicate_handle_rejected():
    with pytest.raises(ValueError, match="Duplicate Handle"):
        build_dry_run_plan(DOC, [rec("A1"), rec("A1")])


def test_cross_document_rejected():
    other = AIASSyncRecord(
        document_key="other",
        aias_id="autocad:other:A1",
        autocad_handle="A1",
        baseline_fingerprint="b",
        aias_fingerprint="b",
        autocad_fingerprint="b",
    )
    with pytest.raises(ValueError, match="document_key"):
        build_dry_run_plan(DOC, [other])


def test_payload_is_explicitly_dry_run():
    payload = plan_to_payload(build_dry_run_plan(DOC, [rec()]))
    assert payload["dry_run"] is True
    assert payload["automatic_autocad_write_count"] == 0
    assert payload["automatic_autocad_delete_count"] == 0


def test_no_vendor_write_surface():
    plan = build_dry_run_plan(DOC, [rec()])
    forbidden = {
        "Save", "SaveAs", "SendCommand", "Dispatch", "CreateObject",
        "save", "save_as", "send_command", "dispatch", "create_object",
        "delete_entity", "update_entity", "create_entity",
    }
    assert forbidden.isdisjoint(set(dir(plan)))
