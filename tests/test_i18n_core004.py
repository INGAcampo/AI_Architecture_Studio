import json
from pathlib import Path

from aias_i18n import I18nCoverageAuditor, get_translator
from gui.project_browser.model import BrowserNode, BrowserNodeKind, ProjectBrowserModel
from gui.property_palette.adapter import default_wall_schema

ROOT = Path(__file__).resolve().parents[1]


def test_core004_catalog_overlays_are_parallel_and_merged():
    es = json.loads((ROOT / "resources/i18n/es-VE.workspace.json").read_text(encoding="utf-8"))
    en = json.loads((ROOT / "resources/i18n/en-US.workspace.json").read_text(encoding="utf-8"))
    assert set(es["messages"]) == set(en["messages"])
    assert len(es["messages"]) >= 40
    assert get_translator("es-VE").translate("property.name") == "Nombre"
    assert get_translator("en-US").translate("property.name") == "Name"


def test_browser_and_property_labels_consume_translation_keys():
    browser = ProjectBrowserModel()
    browser.add_node(BrowserNode("wall-1", "Wall", BrowserNodeKind.OBJECT))
    assert browser.require("wall-1").title == "Wall"
    labels = {item.property_id: item.label for item in default_wall_schema()}
    assert labels["name"] == "Nombre" and labels["area"] == "Área"


def test_core004_measurably_improves_coverage_without_false_completion_claim():
    report = I18nCoverageAuditor().audit(ROOT)
    assert report["hardcoded_candidates"] <= 113
    assert report["translation_key_references"] >= 166
    assert report["full_gui_translation_claimed"] is False
