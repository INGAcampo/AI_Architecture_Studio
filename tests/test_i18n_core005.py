# I18N-CORE-005 BIM Browser Tree localization contract.

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from aias_i18n.runtime import tr

ROOT = Path(__file__).resolve().parents[1]
GROUP_KEYS = ("group.levels", "group.families", "group.materials", "group.phases")


def _builder_source() -> str:
    return (ROOT / "src/gui/bim_workspace/builder.py").read_text(encoding="utf-8")


def test_i18n_core005_runtime_default_locale_is_es_ve() -> None:
    assert inspect.signature(tr).parameters["locale"].default == "es-VE"


def test_i18n_core005_group_keys_resolve_in_supported_base_locales() -> None:
    for locale in ("es-VE", "en-US"):
        for key in GROUP_KEYS:
            assert tr(key, locale) != key


def test_i18n_core005_builder_uses_exact_four_runtime_group_translations() -> None:
    tree = ast.parse(_builder_source())
    calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "tr":
            continue
        if not node.args or not isinstance(node.args[0], ast.Constant):
            continue
        if node.args[0].value in GROUP_KEYS:
            calls.append(node)
    assert len(calls) == 4
    assert {node.args[0].value for node in calls} == set(GROUP_KEYS)


def test_i18n_core005_group_calls_follow_existing_implicit_locale_contract() -> None:
    tree = ast.parse(_builder_source())
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "tr"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value in GROUP_KEYS
        ):
            assert len(node.args) == 1
            assert all(keyword.arg != "locale" for keyword in node.keywords)


def test_i18n_core005_static_group_fallback_labels_are_removed() -> None:
    source = _builder_source()
    for literal in ("Niveles", "Familias", "Materiales", "Fases"):
        assert f'"{literal}"' not in source
        assert f"'{literal}'" not in source


def test_i18n_core005_bim_domain_defaults_remain_data_not_ui_translation() -> None:
    source = _builder_source()
    assert "Nivel 0" in source
    assert "New Construction" in source
