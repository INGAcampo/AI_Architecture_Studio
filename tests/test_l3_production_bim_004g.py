from __future__ import annotations

from dataclasses import dataclass

import pytest

from aias_l3_production_bim.external_connectors import (
    ApplicationAvailability,
    AutoCADConnector,
    ConnectorResult,
    ExternalApplicationState,
    ExternalApplicationUnavailable,
    ExternalConnectorNotConnected,
    ExternalConnectorRegistry,
    Geo5Connector,
    SketchUpConnector,
    build_default_external_connector_registry,
)


class FakeModelBackend:
    def __init__(self, app: str):
        self.app = app
        self.connected = False
        self.closed = False

    def availability(self):
        return ApplicationAvailability(self.app, ExternalApplicationState.AVAILABLE, version="test")

    def connect(self):
        self.connected = True
        return {"session": self.app}

    def close(self):
        self.closed = True
        self.connected = False

    def export_model(self, model, target):
        return {"model": model, "target": target}

    def import_model(self, source):
        return {"source": source}


class FakeGeo5Backend:
    def __init__(self):
        self.connected = False

    def availability(self):
        return ApplicationAvailability("geo5", ExternalApplicationState.AVAILABLE, version="test")

    def connect(self):
        self.connected = True
        return "geo5-session"

    def close(self):
        self.connected = False

    def export_geotechnical_model(self, model, target):
        return {"input": model, "target": target}

    def import_geotechnical_result(self, source):
        return {"result_source": source}


def test_default_registry_does_not_connect_or_launch_external_apps():
    registry = build_default_external_connector_registry()
    snapshot = registry.availability_snapshot()
    assert set(snapshot) == {"autocad", "sketchup", "geo5"}
    assert all(not status.available for status in snapshot.values())
    assert all(not connector.connected for connector in registry.all())


@pytest.mark.parametrize("connector", [AutoCADConnector(), SketchUpConnector(), Geo5Connector()])
def test_default_connector_fails_deterministically_when_vendor_backend_missing(connector):
    assert not connector.availability().available
    with pytest.raises(ExternalApplicationUnavailable):
        connector.connect()


def test_autocad_requires_explicit_connection():
    backend = FakeModelBackend("autocad")
    connector = AutoCADConnector(backend)
    with pytest.raises(ExternalConnectorNotConnected):
        connector.export_model({"id": 1}, "drawing.dwg")
    connector.connect()
    result = connector.export_model({"id": 1}, "drawing.dwg")
    assert isinstance(result, ConnectorResult)
    assert result.success
    assert result.payload["target"] == "drawing.dwg"
    connector.close()
    assert not connector.connected


def test_sketchup_exchange_uses_injected_backend_only():
    backend = FakeModelBackend("sketchup")
    connector = SketchUpConnector(backend)
    connector.connect()
    out = connector.export_model({"mesh": 1}, "model.skp")
    incoming = connector.import_model("model.skp")
    assert out.success and incoming.success
    assert out.payload["target"] == "model.skp"


def test_geo5_keeps_input_and_analysis_result_contracts_separate():
    connector = Geo5Connector(FakeGeo5Backend())
    connector.connect()
    exported = connector.export_geotechnical_model({"soil_profile": 1}, "case")
    imported = connector.import_geotechnical_result("results")
    assert exported.operation == "export_geotechnical_model"
    assert imported.operation == "import_geotechnical_result"
    assert "input" in exported.payload
    assert "result_source" in imported.payload


def test_registry_never_connects_during_registration_or_lookup():
    backend = FakeModelBackend("autocad")
    connector = AutoCADConnector(backend)
    registry = ExternalConnectorRegistry()
    registry.register("autocad", connector)
    assert not backend.connected
    assert registry.get("AUTOCAD") is connector
    assert not backend.connected
