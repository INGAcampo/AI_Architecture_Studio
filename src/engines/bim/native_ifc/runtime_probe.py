"""Deterministic optional-runtime discovery for IfcOpenShell."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.util


@dataclass(frozen=True)
class IfcOpenShellRuntimeProbe:
    module: str
    available: bool

    def to_dict(self) -> dict:
        return asdict(self)


def probe_ifcopenshell_runtime(module: str = "ifcopenshell") -> IfcOpenShellRuntimeProbe:
    name = str(module)
    return IfcOpenShellRuntimeProbe(
        module=name,
        available=importlib.util.find_spec(name) is not None,
    )
