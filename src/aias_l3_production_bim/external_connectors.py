"""Safe external-application connector foundation for AIAS Level 3.

This module intentionally separates a product connector from the vendor runtime
backend that actually talks to AutoCAD, SketchUp, or GEO5.  Importing or
constructing these connectors never launches an external application.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


class ExternalApplicationState(str, Enum):
    """Represent the availability state of an external application backend."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ApplicationAvailability:
    """Describe whether a vendor backend can be used without launching it."""

    application: str
    state: ExternalApplicationState
    detail: str = ""
    version: str | None = None

    @property
    def available(self) -> bool:
        """Return True only when the backend explicitly reports availability."""
        return self.state is ExternalApplicationState.AVAILABLE


@dataclass(frozen=True)
class ConnectorResult:
    """Return a deterministic connector operation result."""

    application: str
    operation: str
    success: bool
    payload: Any = None
    detail: str = ""


class ExternalConnectorError(RuntimeError):
    """Base error raised by AIAS external connector infrastructure."""


class ExternalApplicationUnavailable(ExternalConnectorError):
    """Raise when an operation requires a backend that is unavailable."""


class ExternalConnectorNotConnected(ExternalConnectorError):
    """Raise when an operation requires an explicit connection first."""


@runtime_checkable
class ExternalApplicationBackend(Protocol):
    """Define the backend contract implemented by vendor-specific adapters."""

    def availability(self) -> ApplicationAvailability:
        """Inspect backend availability without launching an application."""
        ...

    def connect(self) -> Any:
        """Connect explicitly to the vendor runtime and return a session."""
        ...

    def close(self) -> None:
        """Close or release the current vendor runtime session."""
        ...


@runtime_checkable
class ModelExchangeBackend(ExternalApplicationBackend, Protocol):
    """Define a generic model import/export backend contract."""

    def export_model(self, model: Any, target: Any) -> Any:
        """Export an AIAS model through the vendor backend."""
        ...

    def import_model(self, source: Any) -> Any:
        """Import a vendor model into an AIAS-neutral representation."""
        ...


@runtime_checkable
class Geo5ExchangeBackend(ExternalApplicationBackend, Protocol):
    """Define a GEO5-specific geotechnical exchange backend contract."""

    def export_geotechnical_model(self, model: Any, target: Any) -> Any:
        """Export explicit geotechnical input data to a GEO5 backend."""
        ...

    def import_geotechnical_result(self, source: Any) -> Any:
        """Import GEO5 analysis results as structured data."""
        ...


class NullExternalBackend:
    """Provide a safe backend that never launches or connects to any product."""

    def __init__(self, application: str, detail: str = "No vendor backend configured.") -> None:
        """Initialize a deterministic unavailable backend for an application."""
        self._application = application
        self._detail = detail

    def availability(self) -> ApplicationAvailability:
        """Report this null backend as unavailable without side effects."""
        return ApplicationAvailability(
            application=self._application,
            state=ExternalApplicationState.UNAVAILABLE,
            detail=self._detail,
        )

    def connect(self) -> Any:
        """Reject connection because no vendor backend is configured."""
        raise ExternalApplicationUnavailable(
            f"{self._application} backend is unavailable: {self._detail}"
        )

    def close(self) -> None:
        """Release no resources because the null backend owns no session."""
        return None

    def export_model(self, model: Any, target: Any) -> Any:
        """Reject generic model export because no backend is configured."""
        raise ExternalApplicationUnavailable(
            f"{self._application} export backend is unavailable."
        )

    def import_model(self, source: Any) -> Any:
        """Reject generic model import because no backend is configured."""
        raise ExternalApplicationUnavailable(
            f"{self._application} import backend is unavailable."
        )

    def export_geotechnical_model(self, model: Any, target: Any) -> Any:
        """Reject GEO5 export because no backend is configured."""
        raise ExternalApplicationUnavailable(
            f"{self._application} geotechnical export backend is unavailable."
        )

    def import_geotechnical_result(self, source: Any) -> Any:
        """Reject GEO5 result import because no backend is configured."""
        raise ExternalApplicationUnavailable(
            f"{self._application} geotechnical result backend is unavailable."
        )


class _SafeConnectorBase:
    """Implement explicit-connect behavior shared by vendor connectors."""

    application_name = "external"

    def __init__(self, backend: ExternalApplicationBackend | None = None) -> None:
        """Initialize without connecting or launching the external application."""
        self._backend = backend or NullExternalBackend(self.application_name)
        self._session: Any = None

    @property
    def connected(self) -> bool:
        """Return whether an explicit connection has produced a live session."""
        return self._session is not None

    def availability(self) -> ApplicationAvailability:
        """Inspect backend availability without connecting or launching it."""
        return self._backend.availability()

    def connect(self) -> Any:
        """Connect explicitly after confirming that the backend is available."""
        status = self.availability()
        if not status.available:
            raise ExternalApplicationUnavailable(
                f"{self.application_name} is unavailable: {status.detail}"
            )
        self._session = self._backend.connect()
        return self._session

    def close(self) -> None:
        """Close the backend session and clear connector connection state."""
        try:
            self._backend.close()
        finally:
            self._session = None

    def _require_connected(self) -> None:
        """Require an explicit connection before a vendor operation is invoked."""
        if not self.connected:
            raise ExternalConnectorNotConnected(
                f"{self.application_name} connector is not connected."
            )


class AutoCADConnector(_SafeConnectorBase):
    """Expose the AIAS AutoCAD connector contract through an injected backend."""

    application_name = "autocad"

    def export_model(self, model: Any, path_or_document: Any) -> ConnectorResult:
        """Export a model through the configured AutoCAD backend."""
        self._require_connected()
        backend = self._backend
        if not isinstance(backend, ModelExchangeBackend):
            raise ExternalConnectorError("AutoCAD backend lacks model exchange contract.")
        payload = backend.export_model(model, path_or_document)
        return ConnectorResult("autocad", "export_model", True, payload)

    def import_model(self, source: Any) -> ConnectorResult:
        """Import an AutoCAD source through the configured backend."""
        self._require_connected()
        backend = self._backend
        if not isinstance(backend, ModelExchangeBackend):
            raise ExternalConnectorError("AutoCAD backend lacks model exchange contract.")
        payload = backend.import_model(source)
        return ConnectorResult("autocad", "import_model", True, payload)


class SketchUpConnector(_SafeConnectorBase):
    """Expose a SketchUp connector contract without fabricating a SketchUp API."""

    application_name = "sketchup"

    def export_model(self, model: Any, target: Any) -> ConnectorResult:
        """Export a model through an explicitly configured SketchUp backend."""
        self._require_connected()
        backend = self._backend
        if not isinstance(backend, ModelExchangeBackend):
            raise ExternalConnectorError("SketchUp backend lacks model exchange contract.")
        payload = backend.export_model(model, target)
        return ConnectorResult("sketchup", "export_model", True, payload)

    def import_model(self, source: Any) -> ConnectorResult:
        """Import a SketchUp source through an explicitly configured backend."""
        self._require_connected()
        backend = self._backend
        if not isinstance(backend, ModelExchangeBackend):
            raise ExternalConnectorError("SketchUp backend lacks model exchange contract.")
        payload = backend.import_model(source)
        return ConnectorResult("sketchup", "import_model", True, payload)


class Geo5Connector(_SafeConnectorBase):
    """Expose GEO5 geotechnical exchange through an injected explicit backend."""

    application_name = "geo5"

    def export_geotechnical_model(self, model: Any, target: Any) -> ConnectorResult:
        """Export geotechnical inputs without conflating them with analysis results."""
        self._require_connected()
        backend = self._backend
        if not isinstance(backend, Geo5ExchangeBackend):
            raise ExternalConnectorError("GEO5 backend lacks geotechnical exchange contract.")
        payload = backend.export_geotechnical_model(model, target)
        return ConnectorResult("geo5", "export_geotechnical_model", True, payload)

    def import_geotechnical_result(self, source: Any) -> ConnectorResult:
        """Import structured GEO5 analysis results separately from input data."""
        self._require_connected()
        backend = self._backend
        if not isinstance(backend, Geo5ExchangeBackend):
            raise ExternalConnectorError("GEO5 backend lacks geotechnical exchange contract.")
        payload = backend.import_geotechnical_result(source)
        return ConnectorResult("geo5", "import_geotechnical_result", True, payload)


class ExternalConnectorRegistry:
    """Store external connectors without connecting to any registered product."""

    def __init__(self) -> None:
        """Initialize an empty connector registry."""
        self._connectors: dict[str, _SafeConnectorBase] = {}

    def register(self, name: str, connector: _SafeConnectorBase) -> None:
        """Register a connector instance under a stable lowercase name."""
        key = name.strip().lower()
        if not key:
            raise ValueError("Connector name must not be empty.")
        self._connectors[key] = connector

    def get(self, name: str) -> _SafeConnectorBase:
        """Return a registered connector without connecting it."""
        key = name.strip().lower()
        try:
            return self._connectors[key]
        except KeyError as exc:
            raise KeyError(f"Unknown external connector: {name}") from exc

    def all(self) -> tuple[_SafeConnectorBase, ...]:
        """Return all registered connectors without changing connection state."""
        return tuple(self._connectors.values())

    def availability_snapshot(self) -> dict[str, ApplicationAvailability]:
        """Return side-effect-free availability information for all connectors."""
        return {
            name: connector.availability()
            for name, connector in self._connectors.items()
        }


def build_default_external_connector_registry() -> ExternalConnectorRegistry:
    """Build the safe default registry with no vendor runtime dependencies."""
    registry = ExternalConnectorRegistry()
    registry.register("autocad", AutoCADConnector())
    registry.register("sketchup", SketchUpConnector())
    registry.register("geo5", Geo5Connector())
    return registry
