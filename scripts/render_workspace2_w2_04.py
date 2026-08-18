"""Render the W2-04 command palette for visual verification."""
from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication
from aias_design_system import render_qss
from gui.workspace2 import CommandPaletteWidget, ProfessionalStatus, core_command_catalog


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    output = root / "workspace2_w2_04_outputs" / "COMMAND_PALETTE_DARK.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    # Qt's offscreen plugin does not enumerate Windows fonts automatically.
    # Register the same system family used by the production theme.
    font_path = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "segoeui.ttf"
    if font_path.is_file() and QFontDatabase.addApplicationFont(str(font_path)) < 0:
        raise RuntimeError("visual_test_font_registration_failed")
    app.setStyleSheet(render_qss("dark"))
    status = ProfessionalStatus(jurisdiction="VE", units="SI", normative_status="NOT_ACQUIRED", review_status="DRAFT")
    widget = CommandPaletteWidget(core_command_catalog(), status)
    widget.setWindowTitle("AIAS — Command Center")
    widget.resize(760, 560)
    widget.show(); app.processEvents()
    if not widget.grab().save(str(output)):
        raise RuntimeError("render_capture_failed")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
