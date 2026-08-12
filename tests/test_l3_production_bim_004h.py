from __future__ import annotations

import pytest

import aias_l3_production_bim.autocad_activex_backend as mod
from aias_l3_production_bim.autocad_activex_backend import (
    AUTOCAD_2025_PROGID,
    AutoCADActiveXBackend,
    AutoCADBackendPolicy,
    AutoCADCapability,
)
from aias_l3_production_bim.external_connectors import ExternalApplicationUnavailable


class FakeDocument:
    pass


class FakeApplication:
    def __init__(self):
        self.ActiveDocument = FakeDocument()
        self.Visible = False


class FakeMapper:
    def export_to_document(self, model, document):
        return {"model": model, "document": document}

    def import_from_document(self, document):
        return {"document": document}


def usable(progid):
    return AutoCADCapability(True, progid, True, True, "test capability")


def unavailable(progid):
    return AutoCADCapability(True, progid, False, False, "unavailable")


def test_004h_v11_official_progid():
    assert AUTOCAD_2025_PROGID == "AutoCAD.Application.25.0"


def test_004h_v11_safe_pywin32_probe_when_parent_missing(monkeypatch):
    def boom(name):
        raise ModuleNotFoundError(name)
    monkeypatch.setattr(mod.importlib.util, "find_spec", boom)
    assert mod._pywin32_available() is False


def test_004h_v11_constructor_no_side_effect():
    calls = []
    b = AutoCADActiveXBackend(
        FakeMapper(),
        get_active_object=lambda p: calls.append(("get", p)),
        create_object=lambda p: calls.append(("create", p)),
        capability_probe=usable,
    )
    assert calls == []
    assert not b.connected


def test_004h_v11_availability_no_dispatch():
    calls = []
    b = AutoCADActiveXBackend(
        FakeMapper(),
        get_active_object=lambda p: calls.append(("get", p)),
        create_object=lambda p: calls.append(("create", p)),
        capability_probe=usable,
    )
    assert b.availability().available
    assert calls == []


def test_004h_v11_attach_only():
    app = FakeApplication()
    calls = []
    b = AutoCADActiveXBackend(
        FakeMapper(),
        policy=AutoCADBackendPolicy(allow_launch=False),
        get_active_object=lambda p: calls.append(("get", p)) or app,
        create_object=lambda p: calls.append(("create", p)),
        capability_probe=usable,
    )
    assert b.connect() is app
    assert calls == [("get", AUTOCAD_2025_PROGID)]
    assert not b.launched_by_backend


def test_004h_v11_no_launch_when_forbidden():
    calls = []
    def getter(p):
        calls.append(("get", p))
        raise RuntimeError("not running")
    b = AutoCADActiveXBackend(
        FakeMapper(),
        policy=AutoCADBackendPolicy(allow_launch=False),
        get_active_object=getter,
        create_object=lambda p: calls.append(("create", p)),
        capability_probe=usable,
    )
    with pytest.raises(ExternalApplicationUnavailable):
        b.connect()
    assert calls == [("get", AUTOCAD_2025_PROGID)]


def test_004h_v11_explicit_launch():
    app = FakeApplication()
    calls = []
    def getter(p):
        calls.append(("get", p))
        raise RuntimeError("not running")
    b = AutoCADActiveXBackend(
        FakeMapper(),
        policy=AutoCADBackendPolicy(allow_launch=True),
        get_active_object=getter,
        create_object=lambda p: calls.append(("create", p)) or app,
        capability_probe=usable,
    )
    assert b.connect() is app
    assert b.launched_by_backend
    assert calls == [
        ("get", AUTOCAD_2025_PROGID),
        ("create", AUTOCAD_2025_PROGID),
    ]


def test_004h_v11_mapper_translation():
    app = FakeApplication()
    b = AutoCADActiveXBackend(
        FakeMapper(),
        get_active_object=lambda p: app,
        create_object=lambda p: app,
        capability_probe=usable,
    )
    b.connect()
    assert b.export_model({"wall": 1})["document"] is app.ActiveDocument
    assert b.import_model()["document"] is app.ActiveDocument


def test_004h_v11_unavailable_blocks_dispatch():
    calls = []
    b = AutoCADActiveXBackend(
        FakeMapper(),
        get_active_object=lambda p: calls.append(("get", p)),
        create_object=lambda p: calls.append(("create", p)),
        capability_probe=unavailable,
    )
    with pytest.raises(ExternalApplicationUnavailable):
        b.connect()
    assert calls == []
