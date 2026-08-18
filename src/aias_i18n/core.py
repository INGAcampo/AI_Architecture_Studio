"""Deterministic locale profiles, catalogs, formatting and Unicode safety."""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

LOCALE_CODE = re.compile(r"^[a-z]{2,3}-[A-Z]{2}$")
BIDI_CONTROLS = {chr(value) for value in (*range(0x202A, 0x202F), *range(0x2066, 0x206A))}


@dataclass(frozen=True, slots=True)
class LocaleProfile:
    """Declare one bounded language-territory presentation profile."""
    code: str
    language: str
    territory: str
    decimal_separator: str
    grouping_separator: str
    date_pattern: str
    unit_system: str = "SI"
    text_direction: str = "LTR"

    def validate(self) -> None:
        if not LOCALE_CODE.fullmatch(self.code) or self.code != f"{self.language}-{self.territory}":
            raise ValueError("invalid_locale_code")
        if self.decimal_separator == self.grouping_separator:
            raise ValueError("ambiguous_numeric_separators")
        if self.text_direction not in {"LTR", "RTL"}:
            raise ValueError("invalid_text_direction")
        if self.unit_system not in {"SI", "US_CUSTOMARY"}:
            raise ValueError("invalid_unit_system")

    def format_decimal(self, value: Decimal | int | float, places: int = 2) -> str:
        """Format a value without changing its engineering meaning."""
        self.validate()
        if places < 0 or places > 12:
            raise ValueError("invalid_decimal_places")
        text = f"{Decimal(str(value)):,.{places}f}"
        return text.replace(",", "\uFFFF").replace(".", self.decimal_separator).replace("\uFFFF", self.grouping_separator)

    def format_date(self, value: date | datetime) -> str:
        """Format an ISO date through the explicit profile pattern."""
        self.validate()
        return value.strftime(self.date_pattern)


@dataclass(frozen=True, slots=True)
class Catalog:
    """Immutable message catalog loaded from a versioned UTF-8 artifact."""
    locale: str
    version: str
    messages: dict[str, str]

    @classmethod
    def load(cls, path: str | Path) -> "Catalog":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        catalog = cls(str(payload["locale"]), str(payload["version"]), dict(payload["messages"]))
        if not LOCALE_CODE.fullmatch(catalog.locale) or not catalog.messages:
            raise ValueError("invalid_message_catalog")
        if any(not key or not isinstance(value, str) or not value for key, value in catalog.messages.items()):
            raise ValueError("invalid_catalog_entry")
        return catalog


class Translator:
    """Resolve stable keys with an explicit fallback and missing-key evidence."""
    def __init__(self, primary: Catalog, fallback: Catalog | None = None, *, strict: bool = False) -> None:
        self.primary, self.fallback, self.strict = primary, fallback, strict
        self.missing: set[str] = set()

    def translate(self, key: str, **values) -> str:
        message = self.primary.messages.get(key)
        if message is None and self.fallback is not None:
            message = self.fallback.messages.get(key)
        if message is None:
            self.missing.add(key)
            if self.strict:
                raise KeyError(f"missing_translation:{key}")
            return f"⟦{key}⟧"
        try:
            return message.format(**values)
        except KeyError as exc:
            raise ValueError(f"missing_translation_parameter:{exc.args[0]}") from exc


def normalize_user_text(value: str, *, allow_multiline: bool = True) -> str:
    """Normalize to NFC and reject invisible bidi overrides used for spoofing."""
    if any(character in BIDI_CONTROLS for character in value):
        raise ValueError("unicode_bidi_control_forbidden")
    normalized = unicodedata.normalize("NFC", value)
    if not allow_multiline and any(character in normalized for character in "\r\n"):
        raise ValueError("multiline_text_forbidden")
    return normalized
