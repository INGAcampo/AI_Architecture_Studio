import json
from pathlib import Path

from aias_i18n import Catalog, I18nCoverageAuditor, Translator
from gui.workspace2 import core_command_catalog

ROOT=Path(__file__).resolve().parents[1]


def test_catalogs_have_exact_key_parity():
    es=Catalog.load(ROOT/"resources/i18n/es-VE.json");en=Catalog.load(ROOT/"resources/i18n/en-US.json")
    assert set(es.messages)==set(en.messages) and len(es.messages)>=46


def test_priority_surfaces_use_keys_not_previous_literals():
    checks={
        "src/gui/project_browser/qt_widget.py":["Buscar niveles, categorías u objetos…","Seleccionar","Expandir","Contraer"],
        "src/gui/workspace2/qt_command_palette.py":["Buscar comando, disciplina o capacidad…","Norma:"],
        "src/gui/project_session.py":["Cambios sin guardar","No se pudo abrir","Proyecto guardado:"],
        "src/gui/property_palette/model.py":["Propiedad desconocida:","Valor booleano no válido:","<varios>"],
    }
    for relative,literals in checks.items():
        source=(ROOT/relative).read_text(encoding="utf-8")
        assert all(literal not in source for literal in literals)


def test_locale_changes_titles_not_command_identity():
    es=core_command_catalog(translator=Translator(Catalog.load(ROOT/"resources/i18n/es-VE.json")))
    en=core_command_catalog(translator=Translator(Catalog.load(ROOT/"resources/i18n/en-US.json")))
    assert es.resolve("WALL").title=="Muro" and en.resolve("WALL").title=="Wall"
    assert es.resolve("WALL").command_id==en.resolve("WALL").command_id=="WALL"


def test_coverage_improves_without_full_coverage_claim():
    report=I18nCoverageAuditor().audit(ROOT)
    assert report["hardcoded_candidates"]<=218 and report["translation_key_references"]>=45
    assert report["hardcoded_candidates"]<255 and report["full_gui_translation_claimed"] is False
