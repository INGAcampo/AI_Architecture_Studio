import pytest

from aias_l3_production_bim.autocad_write_transaction import (
    InMemoryReversibleBackend,
    OperationKind,
    ProductionWriteDisabled,
    ReversibleTransaction,
    TransactionAlreadyClosed,
    TransactionNotActive,
    TransactionState,
    WriteOperation,
)


def line(entity_id="L1"):
    return WriteOperation(
        kind=OperationKind.CREATE_LINE,
        payload={"entity_id": entity_id, "start": (0, 0, 0), "end": (1000, 0, 0)},
    )


def test_begin_enters_active_state():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    assert tx.state is TransactionState.ACTIVE
    assert tx.journal[-1].event == "BEGIN"


def test_apply_requires_active_transaction():
    tx = ReversibleTransaction(InMemoryReversibleBackend())
    with pytest.raises(TransactionNotActive):
        tx.apply(line())


def test_create_then_rollback_restores_empty_backend():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(line())
    assert "L1" in backend.entities
    tx.rollback()
    assert backend.entities == {}
    assert tx.state is TransactionState.ROLLED_BACK


def test_create_then_commit_keeps_entity():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(line())
    tx.commit()
    assert "L1" in backend.entities
    assert tx.state is TransactionState.COMMITTED


def test_delete_then_rollback_restores_entity():
    backend = InMemoryReversibleBackend()
    backend.entities["L1"] = {
        "entity_id": "L1",
        "kind": "line",
        "start": (0, 0, 0),
        "end": (1, 0, 0),
    }
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(WriteOperation(OperationKind.DELETE_ENTITY, {"entity_id": "L1"}))
    assert "L1" not in backend.entities
    tx.rollback()
    assert "L1" in backend.entities


def test_rollback_is_reverse_order():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(line("A"))
    tx.apply(line("B"))
    tx.rollback()
    undo_events = [e for e in backend.events if e[0] == "undo_create"]
    assert undo_events == [("undo_create", "B"), ("undo_create", "A")]


def test_closed_transaction_cannot_rollback_again():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.rollback()
    with pytest.raises(TransactionAlreadyClosed):
        tx.rollback()


def test_production_write_flag_is_rejected():
    tx = ReversibleTransaction(
        InMemoryReversibleBackend(),
        production_write_enabled=True,
    )
    with pytest.raises(ProductionWriteDisabled):
        tx.begin()


def test_transaction_journal_is_serializable():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(line())
    tx.rollback()
    data = tx.to_dict()
    assert data["state"] == "rolled_back"
    assert data["production_write_enabled"] is False
    assert [e["event"] for e in data["journal"]][-1] == "ROLLBACK"


def test_apply_failure_triggers_rollback():
    backend = InMemoryReversibleBackend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(line("L1"))
    with pytest.raises(Exception):
        tx.apply(line("L1"))
    assert tx.state is TransactionState.ROLLED_BACK
    assert backend.entities == {}
