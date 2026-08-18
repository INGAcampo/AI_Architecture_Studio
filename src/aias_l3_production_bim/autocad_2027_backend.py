"""AutoCAD 2027 ActiveX backend for AIAS.

This module is intentionally additive. It does not alter the historical
AutoCAD 2025 backend or its ProgID contract.

The machine-proven authority from AIAS L3 004T/004U is:
    AutoCAD.Application.26

The backend never launches AutoCAD unless ``allow_launch=True`` is explicitly
provided. Attach-only mode uses ``GetActiveObject``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

AUTOCAD_2027_PROGID = "AutoCAD.Application.26"
AUTOCAD_2027_DOCUMENTED_SPECIFIC_PROGID = "AutoCAD.Application.26.0"
AUTOCAD_GENERIC_PROGID = "AutoCAD.Application"


@dataclass(frozen=True)
class AutoCAD2027Availability:
    """Availability state for the AutoCAD 2027 ActiveX backend."""

    pywin32_usable: bool
    registered_authority: str = AUTOCAD_2027_PROGID

    @property
    def usable(self) -> bool:
        """Return whether the Python COM dependency is usable."""
        return self.pywin32_usable


class AutoCAD2027ActiveXBackend:
    """Version-specific AutoCAD 2027 ActiveX backend.

    The default behavior is safe attach-only. Launching through COM is disabled
    unless the caller explicitly opts in with ``allow_launch=True``.
    """

    progid = AUTOCAD_2027_PROGID
    documented_specific_progid = AUTOCAD_2027_DOCUMENTED_SPECIFIC_PROGID
    generic_progid = AUTOCAD_GENERIC_PROGID

    def __init__(
        self,
        *,
        allow_launch: bool = False,
        get_active_object: Callable[[str], Any] | None = None,
        dispatch: Callable[[str], Any] | None = None,
        mapper: Any | None = None,
    ) -> None:
        self.allow_launch = bool(allow_launch)
        self._get_active_object = get_active_object
        self._dispatch = dispatch
        self._mapper = mapper
        self._application: Any | None = None
        self._connected = False
        self._launched = False

    @staticmethod
    def _load_pywin32() -> tuple[Callable[[str], Any], Callable[[str], Any]]:
        import win32com.client  # type: ignore

        return (
            win32com.client.GetActiveObject,
            win32com.client.Dispatch,
        )

    def availability(self) -> AutoCAD2027Availability:
        """Probe pywin32 importability without launching AutoCAD."""
        try:
            self._load_pywin32()
        except Exception:
            return AutoCAD2027Availability(pywin32_usable=False)
        return AutoCAD2027Availability(pywin32_usable=True)

    @property
    def connected(self) -> bool:
        """Whether a live application object is currently attached."""
        return self._connected and self._application is not None

    @property
    def launched(self) -> bool:
        """Whether this backend explicitly launched AutoCAD through Dispatch."""
        return self._launched

    @property
    def application(self) -> Any | None:
        """Return the attached application object, if any."""
        return self._application

    def connect(self) -> Any:
        """Attach to running AutoCAD 2027, optionally launching when explicitly allowed."""
        get_active = self._get_active_object
        dispatch = self._dispatch

        if get_active is None or dispatch is None:
            imported_get, imported_dispatch = self._load_pywin32()
            if get_active is None:
                get_active = imported_get
            if dispatch is None:
                dispatch = imported_dispatch

        try:
            app = get_active(self.progid)
        except Exception:
            if not self.allow_launch:
                raise
            app = dispatch(self.progid)
            self._launched = True

        self._application = app
        self._connected = True
        return app

    def close(self) -> None:
        """Release AIAS references without calling AutoCAD.Quit()."""
        self._application = None
        self._connected = False

    disconnect = close

    def active_document(self) -> Any:
        """Return the current AutoCAD ActiveDocument without modifying it."""
        if not self.connected:
            raise RuntimeError("AutoCAD 2027 backend is not connected.")
        return self._application.ActiveDocument

    def read_document_snapshot(self, *, entity_limit: int = 1000) -> dict[str, Any]:
        """Map the active document into a bounded AIAS-neutral read-only snapshot."""
        document = self.active_document()

        if self._mapper is not None:
            mapper = self._mapper
        else:
            from .autocad_model_mapper import map_document_snapshot
            mapper = map_document_snapshot

        return mapper(document, entity_limit=entity_limit)

    def export_model(self, model: Any) -> Any:
        """Reserved write-path boundary.

        AutoCAD 2027 live write activation is intentionally deferred to a later
        evidence-gated stage.
        """
        raise NotImplementedError(
            "AutoCAD 2027 write/export activation is not enabled in 004V v1.2."
        )

    def import_model(self) -> dict[str, Any]:
        """Read the active AutoCAD document into an AIAS-neutral snapshot."""
        return self.read_document_snapshot()
