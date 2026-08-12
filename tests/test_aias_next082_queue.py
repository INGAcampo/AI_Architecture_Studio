from aias_next082_queue import IntakeQueue

def test_queue_preserves_order_and_pending_state():
    queue = IntakeQueue()
    queue.enqueue({"id": "E-1"})
    queue.enqueue({"id": "E-2"})
    snapshot = queue.snapshot()
    assert [item["id"] for item in snapshot] == ["E-1", "E-2"]
    assert all(item["approved"] is False for item in snapshot)
