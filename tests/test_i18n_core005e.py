# I18N-CORE-005E remaining Workspace localization and refresh readiness.

from __future__ import annotations

import ast
from pathlib import Path

from aias_i18n.runtime import tr

ROOT = Path(__file__).resolve().parents[1]
STATUS_KEYS = (
    "status.layer_visible",
    "status.layer_hidden",
    "status.layer_locked",
    "status.layer_unlocked",
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_i18n_core005e_status_keys_resolve_in_base_locales() -> None:
    for locale in ("es-VE", "en-US"):
        for key in STATUS_KEYS:
            value = tr(key, locale, name="Layer-A")
            assert value != key
            assert "Layer-A" in value


def test_i18n_core005e_main_window_localizes_four_layer_statuses() -> None:
    source = _read("src/gui/main_window.py")
    for key in STATUS_KEYS:
        assert f'self.translator.translate("{key}", name=layer_name)' in source


def test_i18n_core005e_old_layer_status_fstrings_removed() -> None:
    source = _read("src/gui/main_window.py")
    assert 'f"Capa {layer_name} visible"' not in source
    assert 'f"Capa {layer_name} oculta"' not in source
    assert 'f"Capa {layer_name} bloqueada"' not in source
    assert 'f"Capa {layer_name} desbloqueada"' not in source


def test_i18n_core005e_project_browser_tooltip_static_fragments_are_nonlinguistic() -> None:
    tree = ast.parse(_read("src/gui/project_browser/qt_widget.py"))
    tooltip_exprs = []
    metadata_matches = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        short = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id if isinstance(node.func, ast.Name) else None
        if short != "setToolTip" or not node.args:
            continue
        expr = node.args[0]
        tooltip_exprs.append(expr)
        try:
            rendered = ast.unparse(expr)
        except Exception:
            rendered = ""
        if "metadata" in rendered and "category" in rendered:
            metadata_matches.append(expr)
    if len(metadata_matches) == 1:
        candidate = metadata_matches[0]
    else:
        assert len(tooltip_exprs) == 1, (len(tooltip_exprs), len(metadata_matches))
        candidate = tooltip_exprs[0]
    static = "".join(
        n.value for n in ast.walk(candidate)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    )
    assert not any(ch.isalpha() for ch in static), static


def test_i18n_core005e_refresh_surfaces_remain_present() -> None:
    main = ast.parse(_read("src/gui/main_window.py"))
    mf = {n.name for n in ast.walk(main) if isinstance(n, ast.FunctionDef)}
    assert {"refresh_project_tree", "refresh_layers_panel"}.issubset(mf)
    command = ast.parse(_read("src/gui/workspace2/qt_command_palette.py"))
    controller = ast.parse(_read("src/gui/bim_workspace/controller.py"))
    assert "refresh" in {n.name for n in ast.walk(command) if isinstance(n, ast.FunctionDef)}
    assert "refresh" in {n.name for n in ast.walk(controller) if isinstance(n, ast.FunctionDef)}
