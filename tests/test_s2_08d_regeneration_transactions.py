import pytest

from engines.regeneration import (
    DependencyScheduler,
    DirtyTracker,
    RegenerationDependencyCycleError,
    RegenerationEngine,
    RegenerationItem,
    RegenerationQueue,
    RegenerationService,
    RegenerationStatus,
    RegenerationTransaction,
    TransactionManager,
    TransactionOperation,
    TransactionState,
)


@pytest.mark.parametrize("index", range(20))
def test_dirty_tracker_mark_dirty(index):
    tracker = DirtyTracker()
    tracker.mark_dirty(f"o{index}")
    assert tracker.is_dirty(f"o{index}")


@pytest.mark.parametrize("index", range(10))
def test_dirty_tracker_mark_clean(index):
    tracker = DirtyTracker()
    object_id = f"o{index}"
    tracker.mark_dirty(object_id)
    assert tracker.mark_clean(object_id)
    assert not tracker.is_dirty(object_id)


@pytest.mark.parametrize("priority", range(10))
def test_queue_orders_by_priority(priority):
    queue = RegenerationQueue()
    item = RegenerationItem(f"o{priority}", lambda: priority, priority=priority)
    queue.enqueue(item)
    assert queue.dequeue() is item


@pytest.mark.parametrize("count", range(1, 11))
def test_queue_multiple_items(count):
    queue = RegenerationQueue()
    for index in reversed(range(count)):
        queue.enqueue(RegenerationItem(f"o{index}", lambda i=index: i, priority=index))
    ordered = [queue.dequeue().priority for _ in range(count)]
    assert ordered == list(range(count))


@pytest.mark.parametrize("count", range(2, 12))
def test_scheduler_linear_dependencies(count):
    items = []
    for index in range(count):
        deps = (f"o{index - 1}",) if index > 0 else ()
        items.append(RegenerationItem(f"o{index}", lambda: None, dependencies=deps))
    ordered = DependencyScheduler().order(tuple(items))
    assert [item.object_id for item in ordered] == [f"o{index}" for index in range(count)]


@pytest.mark.parametrize("index", range(10))
def test_transaction_operation_undo_redo(index):
    state = {"value": index}
    operation = TransactionOperation(
        redo=lambda: state.__setitem__("value", index + 1),
        undo=lambda: state.__setitem__("value", index),
    )
    operation.redo()
    assert state["value"] == index + 1
    operation.undo()
    assert state["value"] == index


@pytest.mark.parametrize("index", range(10))
def test_transaction_commit(index):
    transaction = RegenerationTransaction(f"t{index}", f"Transaction {index}")
    transaction.commit()
    assert transaction.state is TransactionState.COMMITTED


@pytest.mark.parametrize("index", range(10))
def test_transaction_rollback(index):
    state = {"value": index + 1}
    transaction = RegenerationTransaction(f"t{index}", f"Transaction {index}")
    transaction.add_operation(
        TransactionOperation(
            redo=lambda: None,
            undo=lambda: state.__setitem__("value", index),
        )
    )
    transaction.rollback()
    assert transaction.state is TransactionState.ROLLED_BACK
    assert state["value"] == index


def test_regeneration_item_validation():
    with pytest.raises(ValueError):
        RegenerationItem("", lambda: None)
    with pytest.raises(ValueError):
        RegenerationItem("x", lambda: None, priority=-1)
    with pytest.raises(TypeError):
        RegenerationItem("x", object())


def test_queue_duplicate_rejected():
    queue = RegenerationQueue()
    item = RegenerationItem("x", lambda: None)
    assert queue.enqueue(item)
    assert not queue.enqueue(item)


def test_scheduler_cycle_detection():
    items = (
        RegenerationItem("a", lambda: None, dependencies=("b",)),
        RegenerationItem("b", lambda: None, dependencies=("a",)),
    )
    with pytest.raises(RegenerationDependencyCycleError):
        DependencyScheduler().order(items)


def test_nested_transaction_commit():
    manager = TransactionManager()
    outer = manager.begin("outer")
    inner = manager.begin("inner")
    manager.add_operation(TransactionOperation(lambda: None, lambda: None))
    manager.commit()
    assert inner.state is TransactionState.COMMITTED
    assert len(outer.operations) == 1
    manager.commit()
    assert len(manager.history()) == 1


def test_transaction_context_rolls_back():
    state = {"value": 1}
    manager = TransactionManager()
    with pytest.raises(RuntimeError):
        with manager.transaction("test"):
            manager.add_operation(
                TransactionOperation(
                    redo=lambda: None,
                    undo=lambda: state.__setitem__("value", 0),
                )
            )
            raise RuntimeError("boom")
    assert state["value"] == 0


def test_engine_register_and_regenerate():
    engine = RegenerationEngine()
    engine.register(RegenerationItem("x", lambda: 42))
    results = engine.regenerate()
    assert results[0].value == 42
    assert engine.require("x").status is RegenerationStatus.COMPLETED


def test_engine_dependency_order():
    order = []
    engine = RegenerationEngine()
    engine.register(RegenerationItem("a", lambda: order.append("a"), priority=10))
    engine.register(
        RegenerationItem(
            "b",
            lambda: order.append("b"),
            dependencies=("a",),
            priority=20,
        )
    )
    engine.regenerate()
    assert order == ["a", "b"]


def test_engine_failure_rolls_back():
    engine = RegenerationEngine()
    engine.register(RegenerationItem("a", lambda: 1))
    engine.register(
        RegenerationItem(
            "b",
            lambda: (_ for _ in ()).throw(RuntimeError("boom")),
            dependencies=("a",),
        )
    )
    with pytest.raises(RuntimeError):
        engine.regenerate()
    assert engine.require("a").status is RegenerationStatus.ROLLED_BACK
    assert engine.dirty.is_dirty("a")


def test_engine_events():
    events = []
    engine = RegenerationEngine(
        event_dispatcher=lambda name, payload: events.append((name, payload))
    )
    engine.register(RegenerationItem("x", lambda: 1))
    engine.regenerate()
    assert events[0][0] == "regeneration.item.dirty"
    assert events[-1][0] == "regeneration.completed"


def test_service_register_and_regenerate():
    service = RegenerationService()
    service.register_callback("x", lambda: 7)
    result = service.regenerate_all()[0]
    assert result.value == 7


@pytest.mark.parametrize("index", range(13))
def test_engine_selected_regeneration(index):
    engine = RegenerationEngine()
    engine.register(RegenerationItem(f"o{index}", lambda i=index: i))
    result = engine.regenerate((f"o{index}",))[0]
    assert result.value == index


@pytest.mark.parametrize("index", range(7))
def test_queue_remove_cases(index):
    queue = RegenerationQueue()
    item = RegenerationItem(f"remove-{index}", lambda i=index: i)
    queue.enqueue(item)
    assert queue.remove(item.object_id)
    assert len(queue) == 0
    assert not queue.remove(item.object_id)
