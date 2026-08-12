from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from aias_i18n import Catalog, I18nCoverageAuditor, LocaleProfile, Translator, normalize_user_text
from gui.workspace2 import core_command_catalog

ROOT=Path(__file__).resolve().parents[1]


def profiles():
    return LocaleProfile("es-VE","es","VE",",",".","%d/%m/%Y"),LocaleProfile("en-US","en","US",".",",","%m/%d/%Y","US_CUSTOMARY")


def test_regional_number_date_and_unit_profiles_are_explicit():
    ve,us=profiles();assert ve.format_decimal(Decimal("1234.5"))=="1.234,50";assert us.format_decimal(1234.5)=="1,234.50"
    assert ve.format_date(date(2026,8,4))=="04/08/2026" and us.format_date(date(2026,8,4))=="08/04/2026"


def test_unicode_is_nfc_and_bidi_spoofing_fails_closed():
    assert normalize_user_text("Disen\u0303o") == "Diseño"
    with pytest.raises(ValueError,match="bidi_control"):normalize_user_text("AIAS\u202Eexe")


def test_catalog_fallback_missing_key_and_parameters_are_evidenced():
    es=Catalog.load(ROOT/"resources/i18n/es-VE.json");en=Catalog.load(ROOT/"resources/i18n/en-US.json");translator=Translator(es,en)
    assert translator.translate("command.wall")=="Muro";assert translator.translate("missing.key")=="⟦missing.key⟧";assert translator.missing=={"missing.key"}
    with pytest.raises(KeyError,match="missing_translation"):Translator(es,en,strict=True).translate("missing.key")


def test_workspace_command_catalog_consumes_translator_without_changing_ids():
    translator=Translator(Catalog.load(ROOT/"resources/i18n/es-VE.json"))
    catalog=core_command_catalog(translator=translator)
    assert catalog.resolve("WALL").title=="Muro" and catalog.resolve("WALL").capability_id=="BIM-WALL"
    assert catalog.search("memoria")[0].command_id=="STRUCTURAL-REPORT"


def test_coverage_audit_is_reproducible_and_never_claims_full_translation():
    first=I18nCoverageAuditor().audit(ROOT);second=I18nCoverageAuditor().audit(ROOT)
    assert first["sha256"]==second["sha256"] and first["files_scanned"]>0 and first["hardcoded_candidates"]>0
    assert first["catalog_locales"]==["en-US","es-VE"] and first["translation_key_references"]>=9
    assert first["full_gui_translation_claimed"] is False
