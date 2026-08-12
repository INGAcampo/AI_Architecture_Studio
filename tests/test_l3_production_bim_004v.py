from types import SimpleNamespace

import pytest

from aias_l3_production_bim.autocad_2027_backend import (
    AUTOCAD_2027_PROGID,
    AutoCAD2027ActiveXBackend,
)
from aias_l3_production_bim.autocad_model_mapper import (
    AutoCADAuthority,
    map_collection,
    map_document_snapshot,
    map_entity,
)


class Collection:
    def __init__(self, items):
        self._items = list(items)

    @property
    def Count(self):
        return len(self._items)

    def Item(self, index):
        return self._items[index]


def test_2027_backend_is_additive_and_uses_26():
    assert AUTOCAD_2027_PROGID == "AutoCAD.Application.26"
    assert AutoCAD2027ActiveXBackend.progid == "AutoCAD.Application.26"


def test_2027_attach_only_uses_get_active_and_never_dispatches():
    calls = []

    def get_active(progid):
        calls.append(("get", progid))
        return SimpleNamespace(ActiveDocument=SimpleNamespace(Name="A.dwg"))

    def dispatch(progid):
        calls.append(("dispatch", progid))
        raise AssertionError("Dispatch must not be called in attach-only mode.")

    backend = AutoCAD2027ActiveXBackend(
        allow_launch=False,
        get_active_object=get_active,
        dispatch=dispatch,
    )
    backend.connect()

    assert calls == [("get", "AutoCAD.Application.26")]
    assert backend.connected is True
    assert backend.launched is False


def test_2027_no_launch_when_attach_fails_and_launch_forbidden():
    calls = []

    def get_active(progid):
        calls.append(("get", progid))
        raise RuntimeError("not running")

    def dispatch(progid):
        calls.append(("dispatch", progid))
        return object()

    backend = AutoCAD2027ActiveXBackend(
        allow_launch=False,
        get_active_object=get_active,
        dispatch=dispatch,
    )

    with pytest.raises(RuntimeError):
        backend.connect()

    assert calls == [("get", "AutoCAD.Application.26")]
    assert backend.connected is False
    assert backend.launched is False


def test_2027_explicit_launch_is_separate_from_historical_backend():
    calls = []
    app = SimpleNamespace(ActiveDocument=SimpleNamespace(Name="A.dwg"))

    def get_active(progid):
        calls.append(("get", progid))
        raise RuntimeError("not running")

    def dispatch(progid):
        calls.append(("dispatch", progid))
        return app

    backend = AutoCAD2027ActiveXBackend(
        allow_launch=True,
        get_active_object=get_active,
        dispatch=dispatch,
    )
    assert backend.connect() is app
    assert calls == [
        ("get", "AutoCAD.Application.26"),
        ("dispatch", "AutoCAD.Application.26"),
    ]
    assert backend.launched is True


def test_authority_and_line_mapping():
    authority = AutoCADAuthority()
    assert authority.candidates[0] == "AutoCAD.Application.26"

    entity = SimpleNamespace(
        ObjectName="AcDbLine",
        Handle="AB",
        Layer="A-WALL",
        Color=256,
        Linetype="ByLayer",
        Visible=True,
        StartPoint=(0, 1, 2),
        EndPoint=(3, 4, 5),
    )
    mapped = map_entity(entity)
    assert mapped["kind"] == "line"
    assert mapped["start"] == (0.0, 1.0, 2.0)
    assert mapped["end"] == (3.0, 4.0, 5.0)


def test_polyline_circle_arc_text_block_and_generic_mapping():
    polyline = SimpleNamespace(
        ObjectName="AcDbPolyline", Handle="P", Layer="0", Color=256,
        Linetype="ByLayer", Visible=True, Coordinates=(0, 0, 10, 0),
        Closed=False, Elevation=0,
    )
    circle = SimpleNamespace(
        ObjectName="AcDbCircle", Handle="C", Layer="0", Color=1,
        Linetype="ByLayer", Visible=True, Center=(1, 2, 0), Radius=3,
    )
    arc = SimpleNamespace(
        ObjectName="AcDbArc", Handle="A", Layer="0", Color=1,
        Linetype="ByLayer", Visible=True, Center=(0, 0, 0), Radius=5,
        StartAngle=0.1, EndAngle=1.2,
    )
    text = SimpleNamespace(
        ObjectName="AcDbText", Handle="T", Layer="TEXT", Color=1,
        Linetype="ByLayer", Visible=True, TextString="AIAS",
        InsertionPoint=(4, 5, 0), Height=2.5, Rotation=0,
    )
    block = SimpleNamespace(
        ObjectName="AcDbBlockReference", Handle="B", Layer="BLOCK", Color=1,
        Linetype="ByLayer", Visible=True, EffectiveName="Door",
        InsertionPoint=(7, 8, 0), Rotation=0, XScaleFactor=1,
        YScaleFactor=1, ZScaleFactor=1,
    )
    generic = SimpleNamespace(
        ObjectName="AcDbSomething", Handle="G", Layer="0", Color=1,
        Linetype="ByLayer", Visible=True, Area=9.0,
    )

    assert map_entity(polyline)["kind"] == "polyline"
    assert map_entity(circle)["radius"] == 3.0
    assert map_entity(arc)["kind"] == "arc"
    assert map_entity(text)["text"] == "AIAS"
    assert map_entity(block)["name"] == "Door"
    assert map_entity(generic)["area"] == 9.0


def test_collection_limit_and_document_snapshot():
    items = [
        SimpleNamespace(
            ObjectName="AcDbLine", Handle=str(i), Layer="0", Color=256,
            Linetype="ByLayer", Visible=True, StartPoint=(0, 0, 0),
            EndPoint=(i, 0, 0),
        )
        for i in range(5)
    ]
    assert len(map_collection(Collection(items), limit=2)) == 2

    doc = SimpleNamespace(
        Name="Drawing1.dwg",
        FullName=r"C:\tmp\Drawing1.dwg",
        Path=r"C:\tmp",
        ReadOnly=False,
        Saved=True,
        Layers=Collection([SimpleNamespace(Name="0"), SimpleNamespace(Name="A-WALL")]),
        ModelSpace=Collection([]),
        PaperSpace=Collection([]),
    )
    snapshot = map_document_snapshot(doc)
    assert snapshot["layers"] == ["0", "A-WALL"]
    assert snapshot["authority"] == "AutoCAD.Application.26"
    assert snapshot["mutated"] is False


def test_backend_mapper_injection():
    doc = SimpleNamespace(Name="Drawing1.dwg")
    app = SimpleNamespace(ActiveDocument=doc)

    backend = AutoCAD2027ActiveXBackend(
        get_active_object=lambda progid: app,
        dispatch=lambda progid: None,
        mapper=lambda document, entity_limit=1000: {
            "name": document.Name,
            "limit": entity_limit,
            "mutated": False,
        },
    )
    backend.connect()
    result = backend.read_document_snapshot(entity_limit=25)
    assert result == {"name": "Drawing1.dwg", "limit": 25, "mutated": False}
