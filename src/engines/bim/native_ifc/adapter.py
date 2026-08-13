"""Stable AIAS-side contract for future IfcOpenShell native IFC services."""

from __future__ import annotations

from dataclasses import dataclass

from .runtime_probe import IfcOpenShellRuntimeProbe, probe_ifcopenshell_runtime


class IfcOpenShellUnavailableError(RuntimeError):
    """Raised when native IFC functionality is requested without IfcOpenShell."""


@dataclass(frozen=True)
class NativeIfcAdapter:
    probe: IfcOpenShellRuntimeProbe

    @classmethod
    def discover(cls) -> "NativeIfcAdapter":
        return cls(probe=probe_ifcopenshell_runtime())

    @property
    def available(self) -> bool:
        return self.probe.available

    def require_runtime(self) -> str:
        if not self.probe.available:
            raise IfcOpenShellUnavailableError(
                "IfcOpenShell is not available. "
                "Dependency bootstrap must pass before native IFC operations are enabled."
            )
        return self.probe.module
