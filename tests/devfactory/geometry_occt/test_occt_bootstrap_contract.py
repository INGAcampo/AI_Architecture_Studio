from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from engines.geometry.occt.adapter import OCCTGeometryAdapter, OCCTUnavailableError
from engines.geometry.occt.runtime_probe import OCCTRuntimeProbe, probe_occt_runtime


def test_probe_is_deterministic_for_missing_candidate():
    result = probe_occt_runtime(("aias_nonexistent_occt_binding",))
    assert result == OCCTRuntimeProbe(
        selected_module=None,
        available=False,
        candidates=("aias_nonexistent_occt_binding",),
    )


def test_probe_matches_environment_for_standard_candidates():
    result = probe_occt_runtime()
    expected = next(
        (name for name in ("OCC", "OCP", "OCCT") if importlib.util.find_spec(name) is not None),
        None,
    )
    assert result.selected_module == expected
    assert result.available is (expected is not None)


def test_adapter_fails_closed_without_runtime():
    adapter = OCCTGeometryAdapter(
        probe=OCCTRuntimeProbe(
            selected_module=None,
            available=False,
            candidates=("OCC", "OCP", "OCCT"),
        )
    )
    try:
        adapter.require_runtime()
    except OCCTUnavailableError as exc:
        assert "Dependency bootstrap must pass" in str(exc)
    else:
        raise AssertionError("Expected OCCTUnavailableError")
