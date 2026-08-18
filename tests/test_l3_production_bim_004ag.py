import pytest

from aias_l3_production_bim.autocad_write_transaction import (
    OperationKind,
    ReversibleTransaction,
    WriteOperation,
)
from aias_l3_production_bim.autocad_live_transaction_adapter import (
    AutoCADTemporaryDocumentTransactionBackend,
)


class FakeVariant:
    def __init__(self, _type, value):
        self.value = tuple(value)


class FakeWin32:
    VARIANT = FakeVariant


class FakePythonCom:
    VT_ARRAY = 0x2000
    VT_R8 = 5


class FakeEntity:
    def __init__(self, owner, handle, start, end):
        self.owner = owner
        self.Handle = handle
        self.ObjectName = "AcDbLine"
        self.Layer = "0"
        self.StartPoint = tuple(start)
        self.EndPoint = tuple(end)
        self.deleted = False

    def Delete(self):
        if not self.deleted:
            self.deleted = True
            self.owner.entities.pop(self.Handle, None)


class FakeModelSpace:
    def __init__(self, doc):
        self.doc = doc

    @property
    def Count(self):
        return len(self.doc.entities)

    def AddLine(self, p1, p2):
        handle = f"{len(self.doc.entities)+1:X}"
        e = FakeEntity(self.doc, handle, p1.value, p2.value)
        self.doc.entities[handle] = e
        return e


class FakeDocument:
    def __init__(self):
        self.entities = {}
        self.ModelSpace = FakeModelSpace(self)
        self.closed_with = None

    def HandleToObject(self, handle):
        return self.entities[handle]

    def Close(self, save):
        self.closed_with = save


def make_backend():
    doc = FakeDocument()
    backend = AutoCADTemporaryDocumentTransactionBackend(
        doc,
        pythoncom_module=FakePythonCom,
        win32com_client_module=FakeWin32,
    )
    return doc, backend


def op():
    return WriteOperation(
        OperationKind.CREATE_LINE,
        {"start": (0, 0, 0), "end": (1000, 0, 0)},
    )


def test_live_adapter_create_and_transaction_rollback():
    doc, backend = make_backend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    applied = tx.apply(op())
    assert doc.ModelSpace.Count == 1
    assert applied.result["object_name"] == "AcDbLine"
    tx.rollback()
    assert doc.ModelSpace.Count == 0


def test_rollback_deletes_by_handle():
    doc, backend = make_backend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    applied = tx.apply(op())
    handle = applied.result["handle"]
    assert handle in doc.entities
    tx.rollback()
    assert handle not in doc.entities
    assert ("rollback_delete", handle) in backend.events


def test_close_without_save_requires_no_active_transaction():
    doc, backend = make_backend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    with pytest.raises(Exception):
        backend.close_without_save()
    tx.rollback()
    backend.close_without_save()
    assert doc.closed_with is False


def test_commit_does_not_delete_entity():
    doc, backend = make_backend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(op())
    tx.commit()
    assert doc.ModelSpace.Count == 1


def test_non_line_operation_is_rejected():
    doc, backend = make_backend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    with pytest.raises(NotImplementedError):
        tx.apply(WriteOperation(OperationKind.DELETE_ENTITY, {"entity_id": "X"}))
    assert tx.state.value == "rolled_back"


def test_event_sequence_contains_transactional_rollback():
    doc, backend = make_backend()
    tx = ReversibleTransaction(backend)
    tx.begin()
    tx.apply(op())
    tx.rollback()
    names = [e[0] for e in backend.events]
    assert names == ["begin", "create_line", "rollback_delete", "rollback"]
