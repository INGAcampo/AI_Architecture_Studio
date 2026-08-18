"""Pruebas del Sprint S2.03C.1: launcher e imports normalizados."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_launcher():
    spec = importlib.util.spec_from_file_location("aias_launcher", ROOT / "run.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_launcher_bootstrap_places_src_first(monkeypatch):
    launcher = _load_launcher()
    src = str((ROOT / "src").resolve())
    monkeypatch.setattr(sys, "path", [p for p in sys.path if p != src])

    result = launcher.bootstrap_paths()

    assert result == (ROOT / "src").resolve()
    assert sys.path[0] == src


def test_launcher_bootstrap_is_idempotent():
    launcher = _load_launcher()
    src = str((ROOT / "src").resolve())

    launcher.bootstrap_paths()
    launcher.bootstrap_paths()

    assert sys.path.count(src) == 1


def test_runtime_modules_use_canonical_top_level_imports():
    inspected = [
        ROOT / "src/storage/loader.py",
        ROOT / "src/storage/project_io.py",
        ROOT / "src/gui/project_session.py",
        ROOT / "src/models/project/project_document.py",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in inspected)

    assert "from src." not in combined
    assert "import src." not in combined
