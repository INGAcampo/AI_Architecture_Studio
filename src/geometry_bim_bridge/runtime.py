from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeAvailability:
    ifcopenshell: bool
    occt: bool
    ifcopenshell_version: str | None
    occt_version: str | None


def discover_runtime() -> RuntimeAvailability:
    ifc_ok = False
    ifc_version = None
    occt_ok = False
    occt_version = None

    try:
        import ifcopenshell

        ifc_ok = True
        ifc_version = getattr(ifcopenshell, "version", None)
    except Exception:
        pass

    try:
        import OCP

        occt_ok = True
        occt_version = getattr(OCP, "__version__", None)
    except Exception:
        pass

    return RuntimeAvailability(
        ifcopenshell=ifc_ok,
        occt=occt_ok,
        ifcopenshell_version=ifc_version,
        occt_version=occt_version,
    )
