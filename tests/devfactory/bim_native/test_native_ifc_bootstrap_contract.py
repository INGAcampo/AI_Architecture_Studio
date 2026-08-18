from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from engines.bim.native_ifc.adapter import NativeIfcAdapter, IfcOpenShellUnavailableError
from engines.bim.native_ifc.runtime_probe import IfcOpenShellRuntimeProbe, probe_ifcopenshell_runtime


def test_probe_is_deterministic_for_missing_module():
    result = probe_ifcopenshell_runtime("aias_nonexistent_ifcopenshell")
    assert result == IfcOpenShellRuntimeProbe(
        module="aias_nonexistent_ifcopenshell",
        available=False,
    )


def test_probe_matches_environment():
    result = probe_ifcopenshell_runtime()
    assert result.available is (importlib.util.find_spec("ifcopenshell") is not None)


def test_adapter_fails_closed_without_runtime():
    adapter = NativeIfcAdapter(
        probe=IfcOpenShellRuntimeProbe(module="ifcopenshell", available=False)
    )
    try:
        adapter.require_runtime()
    except IfcOpenShellUnavailableError as exc:
        assert "Dependency bootstrap must pass" in str(exc)
    else:
        raise AssertionError("Expected IfcOpenShellUnavailableError")
