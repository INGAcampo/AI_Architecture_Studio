"""AutoCAD 2025 ActiveX backend for AIAS external connector infrastructure."""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import platform
from typing import Any, Callable, Protocol, runtime_checkable

from .external_connectors import (
    ApplicationAvailability,
    ExternalApplicationState,
    ExternalApplicationUnavailable,
)

AUTOCAD_2025_PROGID = "AutoCAD.Application.25.0"


@dataclass(frozen=True)
class AutoCADBackendPolicy:
    """Control whether AIAS may attach to or launch an AutoCAD process."""

    attach_to_running: bool = True
    allow_launch: bool = False
    visible_on_launch: bool = True


@dataclass(frozen=True)
class AutoCADCapability:
    """Describe host-side capability for the AutoCAD 2025 ActiveX backend."""

    platform_supported: bool
    progid: str
    progid_registered: bool
    pywin32_available: bool
    detail: str

    @property
    def usable(self) -> bool:
        """Return whether the host has the prerequisites for ActiveX access."""
        return (
            self.platform_supported
            and self.progid_registered
            and self.pywin32_available
        )


@runtime_checkable
class AutoCADModelMapper(Protocol):
    """Translate between AIAS models and an AutoCAD ActiveX document."""

    def export_to_document(self, model: Any, document: Any) -> Any:
        """Write an AIAS model into an existing AutoCAD document."""
        ...

    def import_from_document(self, document: Any) -> Any:
        """Read an AutoCAD document into an AIAS-neutral model."""
        ...


def _is_windows() -> bool:
    """Return True when the current host is Windows."""
    return platform.system().lower() == "windows"


def _progid_registered(progid: str) -> bool:
    """Check the Windows registry for a COM ProgID without starting AutoCAD."""
    if not _is_windows():
        return False
    try:
        import winreg
    except ImportError:
        return False

    candidates = (
        (winreg.HKEY_CLASSES_ROOT, progid),
        (winreg.HKEY_CURRENT_USER, rf"Software\Classes\{progid}"),
        (winreg.HKEY_LOCAL_MACHINE, rf"Software\Classes\{progid}"),
    )
    for hive, key in candidates:
        try:
            with winreg.OpenKey(hive, key):
                return True
        except OSError:
            continue
    return False


def _pywin32_available() -> bool:
    """Check pywin32 availability safely when the parent package is absent."""
    try:
        return importlib.util.find_spec("win32com.client") is not None
    except (ModuleNotFoundError, ImportError, AttributeError, ValueError):
        return False


def probe_autocad_2025_capability(
    progid: str = AUTOCAD_2025_PROGID,
) -> AutoCADCapability:
    """Probe ActiveX prerequisites without connecting to or launching AutoCAD."""
    windows = _is_windows()
    registered = _progid_registered(progid) if windows else False
    pywin32 = _pywin32_available() if windows else False

    details: list[str] = []
    if not windows:
        details.append("AutoCAD ActiveX is supported only on Windows.")
    if windows and not registered:
        details.append(f"COM ProgID {progid!r} is not registered.")
    if windows and not pywin32:
        details.append("Optional Python dependency pywin32 is not available.")
    if windows and registered and pywin32:
        details.append("AutoCAD 2025 ActiveX prerequisites detected.")

    return AutoCADCapability(
        platform_supported=windows,
        progid=progid,
        progid_registered=registered,
        pywin32_available=pywin32,
        detail=" ".join(details),
    )


class AutoCADActiveXBackend:
    """Implement the AIAS AutoCAD backend against the Windows ActiveX API."""

    def __init__(
        self,
        mapper: AutoCADModelMapper,
        *,
        progid: str = AUTOCAD_2025_PROGID,
        policy: AutoCADBackendPolicy | None = None,
        get_active_object: Callable[[str], Any] | None = None,
        create_object: Callable[[str], Any] | None = None,
        capability_probe: Callable[[str], AutoCADCapability] | None = None,
    ) -> None:
        """Initialize without connecting to or launching AutoCAD."""
        self._mapper = mapper
        self._progid = progid
        self._policy = policy or AutoCADBackendPolicy()
        self._get_active_object = get_active_object
        self._create_object = create_object
        self._capability_probe = capability_probe or probe_autocad_2025_capability
        self._application: Any = None
        self._launched_by_backend = False

    @property
    def application(self) -> Any:
        """Return the connected AutoCAD application object, if any."""
        return self._application

    @property
    def connected(self) -> bool:
        """Return whether this backend holds an AutoCAD application."""
        return self._application is not None

    @property
    def launched_by_backend(self) -> bool:
        """Return whether this backend explicitly created the AutoCAD instance."""
        return self._launched_by_backend

    def availability(self) -> ApplicationAvailability:
        """Report ActiveX capability without connecting to or launching AutoCAD."""
        capability = self._capability_probe(self._progid)
        return ApplicationAvailability(
            application="autocad",
            state=(
                ExternalApplicationState.AVAILABLE
                if capability.usable
                else ExternalApplicationState.UNAVAILABLE
            ),
            detail=capability.detail,
            version="2025" if capability.progid == AUTOCAD_2025_PROGID else None,
        )

    def _resolve_dispatchers(self) -> tuple[Callable[[str], Any], Callable[[str], Any]]:
        """Load pywin32 dispatch functions only at explicit connection time."""
        if self._get_active_object is not None and self._create_object is not None:
            return self._get_active_object, self._create_object

        try:
            import win32com.client
        except ImportError as exc:
            raise ExternalApplicationUnavailable(
                "pywin32 is required for the AutoCAD ActiveX backend."
            ) from exc

        getter = self._get_active_object or win32com.client.GetActiveObject
        creator = self._create_object or win32com.client.Dispatch
        return getter, creator

    def connect(self) -> Any:
        """Attach to running AutoCAD or launch only when policy explicitly permits."""
        status = self.availability()
        if not status.available:
            raise ExternalApplicationUnavailable(
                f"AutoCAD 2025 ActiveX backend unavailable: {status.detail}"
            )

        getter, creator = self._resolve_dispatchers()
        attach_error: Exception | None = None

        if self._policy.attach_to_running:
            try:
                self._application = getter(self._progid)
                self._launched_by_backend = False
                return self._application
            except Exception as exc:
                attach_error = exc

        if not self._policy.allow_launch:
            detail = (
                f" No running instance was attached: {attach_error}"
                if attach_error is not None else ""
            )
            raise ExternalApplicationUnavailable(
                "No usable running AutoCAD instance and launch policy is disabled."
                + detail
            )

        self._application = creator(self._progid)
        self._launched_by_backend = True
        try:
            self._application.Visible = bool(self._policy.visible_on_launch)
        except Exception:
            pass
        return self._application

    def close(self) -> None:
        """Release the COM reference without terminating a user AutoCAD session."""
        self._application = None
        self._launched_by_backend = False

    def active_document(self) -> Any:
        """Return ActiveDocument from the explicitly connected application."""
        if self._application is None:
            raise ExternalApplicationUnavailable("AutoCAD backend is not connected.")
        try:
            return self._application.ActiveDocument
        except Exception as exc:
            raise ExternalApplicationUnavailable(
                "Connected AutoCAD instance has no accessible ActiveDocument."
            ) from exc

    def export_model(self, model: Any, target: Any = None) -> Any:
        """Export through the injected mapper into the active AutoCAD document."""
        return self._mapper.export_to_document(model, self.active_document())

    def import_model(self, source: Any = None) -> Any:
        """Import through the injected mapper from the active AutoCAD document."""
        return self._mapper.import_from_document(self.active_document())
