from __future__ import annotations

import pytest

from aias_l3_production_bim.autocad_controlled_mutation_transaction import (
    ControlledMutationTransaction,
    InMemoryControlledMutationBackend,
    MutationKind,
    MutationState,
)


def make_backend():
    return InMemoryControlledMutationBackend(
        {
            "A1": {
                "object_name": "AcDbLine",
                "layer": "vista",
                "geometry": {"start": (0.0, 0.0, 0.0), "end": (1.0, 0.0, 0.0)},
                "properties": {"color": 256},
            },
            "A2": {
                "object_name": "AcDbLine",
                "layer": "vista",
                "geometry": {"start": (1.0, 0.0, 0.0), "end": (2.0, 0.0, 0.0)},
                "properties": {"color": 256},
            },
        }
    )


def test_update_rollback_restores_exact_snapshot():
    backend = make_backend()
    before = backend.snapshot("A1")

    tx = ControlledMutationTransaction(backend)
    tx.begin()
    token = tx.update("A1", {"layer": "TEMP", "properties": {"color": 1}})

    assert token.kind is MutationKind.UPDATE_ENTITY
    assert backend.snapshot("A1") != before

    tx.rollback()

    assert tx.state is MutationState.ROLLED_BACK
    assert backend.snapshot("A1") == before
    assert [e.event for e in tx.journal] == [
        "BEGIN", "APPLY", "ROLLBACK_OPERATION", "ROLLBACK"
    ]


def test_delete_rollback_restores_entity():
    backend = make_backend()
    before = backend.snapshot("A1")

    tx = ControlledMutationTransaction(backend)
    tx.begin()
    token = tx.delete("A1")

    assert token.kind is MutationKind.DELETE_ENTITY
    assert "A1" not in backend.entities

    tx.rollback()

    assert backend.snapshot("A1") == before
    assert tx.state is MutationState.ROLLED_BACK


def test_mixed_update_delete_rolls_back_reverse_order():
    backend = make_backend()
    a1_before = backend.snapshot("A1")
    a2_before = backend.snapshot("A2")

    tx = ControlledMutationTransaction(backend)
    tx.begin()
    tx.update("A1", {"layer": "TEMP"})
    tx.delete("A2")
    tx.rollback()

    assert backend.snapshot("A1") == a1_before
    assert backend.snapshot("A2") == a2_before
    rollback_handles = [
        e.handle for e in tx.journal if e.event == "ROLLBACK_OPERATION"
    ]
    assert rollback_handles == ["A2", "A1"]


def test_update_requires_nonempty_changes():
    backend = make_backend()
    tx = ControlledMutationTransaction(backend)
    tx.begin()
    with pytest.raises(ValueError):
        tx.update("A1", {})


def test_update_failure_auto_rolls_back_prior_operations():
    backend = make_backend()
    a1_before = backend.snapshot("A1")
    a2_before = backend.snapshot("A2")

    tx = ControlledMutationTransaction(backend)
    tx.begin()
    tx.update("A1", {"layer": "TEMP"})
    backend.fail_next_update = True

    with pytest.raises(RuntimeError, match="Injected update failure"):
        tx.update("A2", {"layer": "TEMP2"})

    assert tx.state is MutationState.ROLLED_BACK
    assert backend.snapshot("A1") == a1_before
    assert backend.snapshot("A2") == a2_before


def test_delete_failure_auto_rolls_back_prior_operations():
    backend = make_backend()
    a1_before = backend.snapshot("A1")

    tx = ControlledMutationTransaction(backend)
    tx.begin()
    tx.update("A1", {"layer": "TEMP"})
    backend.fail_next_delete = True

    with pytest.raises(RuntimeError, match="Injected delete failure"):
        tx.delete("A2")

    assert tx.state is MutationState.ROLLED_BACK
    assert backend.snapshot("A1") == a1_before
    assert "A2" in backend.entities


def test_commit_keeps_changes_and_blocks_rollback():
    backend = make_backend()
    tx = ControlledMutationTransaction(backend)
    tx.begin()
    tx.update("A1", {"layer": "COMMITTED"})
    tx.commit()

    assert tx.state is MutationState.COMMITTED
    assert backend.snapshot("A1").layer == "COMMITTED"
    with pytest.raises(RuntimeError):
        tx.rollback()


def test_operations_require_active_state():
    backend = make_backend()
    tx = ControlledMutationTransaction(backend)

    with pytest.raises(RuntimeError):
        tx.update("A1", {"layer": "TEMP"})
    with pytest.raises(RuntimeError):
        tx.delete("A1")


def test_snapshot_captures_geometry_and_properties():
    backend = make_backend()
    snap = backend.snapshot("A1")

    assert snap.handle == "A1"
    assert snap.object_name == "AcDbLine"
    assert snap.layer == "vista"
    assert snap.geometry["start"] == (0.0, 0.0, 0.0)
    assert snap.properties["color"] == 256


def test_contract_interface_has_no_persistence_methods():
    backend = make_backend()
    forbidden = {"Save", "SaveAs", "SendCommand", "save", "save_as", "send_command"}
    assert forbidden.isdisjoint(set(dir(backend)))
