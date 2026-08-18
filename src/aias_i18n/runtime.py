"""Cached application-level translation access without global mutable catalogs."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from .core import Catalog,Translator

ROOT=Path(__file__).resolve().parents[2]

@lru_cache(maxsize=8)
def get_translator(locale:str="es-VE",*,strict:bool=False)->Translator:
    primary=_merged(locale);fallback=None if locale=="en-US" else _merged("en-US");return Translator(primary,fallback,strict=strict)

def _merged(locale:str)->Catalog:
    base=Catalog.load(ROOT/"resources/i18n"/f"{locale}.json");messages=dict(base.messages);versions=[base.version]
    for path in sorted((ROOT/"resources/i18n").glob(f"{locale}.*.json")):
        overlay=Catalog.load(path)
        overlap=set(messages)&set(overlay.messages)
        if overlap:raise ValueError("duplicate_translation_keys:"+",".join(sorted(overlap)))
        messages.update(overlay.messages);versions.append(overlay.version)
    return Catalog(locale,"+".join(versions),messages)

def tr(key:str,locale:str="es-VE",**values)->str:
    """Translate one stable key through a cached locale catalog."""
    return get_translator(locale).translate(key,**values)
