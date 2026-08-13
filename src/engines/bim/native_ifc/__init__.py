"""AIAS optional native IFC integration namespace."""

from .runtime_probe import IfcOpenShellRuntimeProbe, probe_ifcopenshell_runtime
from .adapter import NativeIfcAdapter, IfcOpenShellUnavailableError

__all__ = [
    "IfcOpenShellRuntimeProbe",
    "probe_ifcopenshell_runtime",
    "NativeIfcAdapter",
    "IfcOpenShellUnavailableError",
]
