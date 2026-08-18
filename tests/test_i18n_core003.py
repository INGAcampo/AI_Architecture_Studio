import json
from pathlib import Path
from aias_i18n import I18nCoverageAuditor,get_translator

ROOT=Path(__file__).resolve().parents[1]

def test_main_catalog_overlays_have_exact_parity():
    es=json.loads((ROOT/"resources/i18n/es-VE.main.json").read_text(encoding="utf-8"));en=json.loads((ROOT/"resources/i18n/en-US.main.json").read_text(encoding="utf-8"))
    assert set(es["messages"])==set(en["messages"]);assert len(es["messages"])>=70
    assert set(get_translator("es-VE").primary.messages)==set(get_translator("en-US").primary.messages)

def test_main_window_consumes_keys_and_removes_previous_ui_literals():
    source=(ROOT/"src/gui/main_window.py").read_text(encoding="utf-8")
    for literal in ("Nuevo Proyecto","LINE activo: especifica","Explorador del Proyecto","Asistente IA","Ningún objeto seleccionado"):
        assert literal not in source
    for key in ("menu.new_project","cad.line.active","panel.project_explorer","panel.ai_assistant","status.no_selection"):
        assert key in source

def test_new_project_dialog_consumes_keys_and_preserves_standard_names():
    source=(ROOT/"src/gui/dialogs/new_project_dialog.py").read_text(encoding="utf-8")
    assert "Nuevo Proyecto AIAS" not in source and "new_project.title" in source
    for designation in ("ACI 318","AISC 360","ASCE 7","Eurocode"):
        assert designation in source

def test_main_window_phase_measurably_improves_coverage():
    report=I18nCoverageAuditor().audit(ROOT)
    assert report["hardcoded_candidates"]<=163 and report["translation_key_references"]>=117
    assert report["full_gui_translation_claimed"] is False
