from pathlib import Path
import pytest

from gui.workspace2 import Workspace2Shell


ROOT = Path(__file__).resolve().parents[1]


def test_shell_defaults_are_explicit_and_recoverable():
    shell = Workspace2Shell()
    snapshot = shell.snapshot()
    assert snapshot["jurisdiction"] == "VE"
    assert snapshot["profile"] == "Architecture"
    assert len(snapshot["visible_regions"]) == 6


def test_profile_and_theme_fail_closed():
    shell = Workspace2Shell()
    shell.switch_profile("Structure")
    shell.set_theme("light")
    assert shell.snapshot()["theme"] == "light"
    with pytest.raises(ValueError, match="unsupported_workspace_profile"):
        shell.switch_profile("Fantasy")
    with pytest.raises(ValueError, match="unsupported_theme"):
        shell.set_theme("neon")


def test_main_window_uses_governed_qss_and_retains_compatibility_entrypoint():
    source = (ROOT / "src/gui/main_window.py").read_text(encoding="utf-8")
    assert "from aias_design_system import render_qss" in source
    assert "self.setStyleSheet(render_qss(theme))" in source
    assert "def apply_dark_theme(self):" in source
    assert "#2b2b2b" not in source
