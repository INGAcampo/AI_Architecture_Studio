from pathlib import Path


def test_main_window_contains_project_actions():
    source = Path("src/gui/main_window.py").read_text(encoding="utf-8")
    for token in ("Ctrl+N", "Ctrl+O", "Ctrl+S", "Ctrl+Shift+S", "closeEvent"):
        assert token in source
