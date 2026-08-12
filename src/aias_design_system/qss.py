"""Qt Style Sheet projection of semantic AIAS design tokens."""
from __future__ import annotations
from .tokens import design_tokens,validate_tokens

def render_qss(theme:str="dark")->str:
    tokens=design_tokens()
    if validate_tokens(tokens):raise ValueError("invalid_design_tokens")
    if theme not in {"dark","light"}:raise ValueError("unsupported_theme")
    c=tokens[theme]
    # Segoe UI ships with the initial Windows target. Inter remains a branded
    # optional asset; selecting a missing font directly can produce tofu glyphs
    # in Qt's offscreen and installer environments.
    font="Segoe UI"
    return f'''/* AIAS Design System {tokens["version"]} — generated; do not hand-edit */
QWidget {{ background-color: {c["background"]}; color: {c["text"]}; font-family: "{font}", "Segoe UI", sans-serif; font-size: 13px; }}
QMainWindow, QDialog {{ background-color: {c["background"]}; }}
QMenuBar, QMenu, QStatusBar, QToolBar {{ background-color: {c["surface"]}; color: {c["text"]}; border-color: {c["border"]}; }}
QDockWidget::title {{ background-color: {c["surface_elevated"]}; padding: 8px; }}
QTreeView, QListView, QTableView, QTextEdit, QLineEdit, QComboBox {{ background-color: {c["surface"]}; color: {c["text"]}; border: 1px solid {c["border"]}; border-radius: 4px; padding: 6px; selection-background-color: {c["selection"]}; }}
QPushButton {{ background-color: {c["surface_elevated"]}; color: {c["text"]}; border: 1px solid {c["border"]}; border-radius: 4px; min-height: 32px; padding: 4px 12px; }}
QPushButton:hover {{ border-color: {c["accent"]}; }}
QPushButton:pressed {{ background-color: {c["selection"]}; }}
QPushButton:focus, QLineEdit:focus, QTreeView:focus, QComboBox:focus {{ border: 2px solid {c["focus"]}; }}
QPushButton[role="primary"] {{ background-color: {c["accent"]}; color: {c["on_accent"]}; border-color: {c["accent"]}; font-weight: 600; }}
QLabel[role="muted"] {{ color: {c["text_muted"]}; }}
QLabel[state="success"] {{ color: {c["success"]}; }}
QLabel[state="warning"] {{ color: {c["warning"]}; }}
QLabel[state="danger"] {{ color: {c["danger"]}; }}
'''
