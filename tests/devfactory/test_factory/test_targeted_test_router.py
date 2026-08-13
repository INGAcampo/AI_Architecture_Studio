from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from dev_factory.test_factory.router import classify_path, select_test_roots


def test_geometry_route():
    assert classify_path("src/engines/geometry/occt/adapter.py") == "tests/devfactory/geometry_occt"


def test_bim_route_with_windows_slashes():
    assert classify_path(r"src\engines\bim\native_ifc\adapter.py") == "tests/devfactory/bim_native"


def test_unrouted_is_explicit():
    assert classify_path("src/gui/main_window.py") == "UNROUTED"


def test_selection_is_unique_and_deterministic():
    result = select_test_roots(
        [
            "src/engines/bim/native_ifc/adapter.py",
            "src/engines/geometry/occt/adapter.py",
            "src/engines/geometry/occt/runtime_probe.py",
            "docs/readme.md",
        ]
    )
    assert result == (
        "tests/devfactory/bim_native",
        "tests/devfactory/geometry_occt",
    )
