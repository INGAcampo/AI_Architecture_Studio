"""Deterministic optional-runtime discovery for OCCT Python bindings."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.util
from typing import Iterable


DEFAULT_CANDIDATES = ("OCC", "OCP", "OCCT")


@dataclass(frozen=True)
class OCCTRuntimeProbe:
    selected_module: str | None
    available: bool
    candidates: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def probe_occt_runtime(candidates: Iterable[str] = DEFAULT_CANDIDATES) -> OCCTRuntimeProbe:
    names = tuple(str(name) for name in candidates)
    selected = next((name for name in names if importlib.util.find_spec(name) is not None), None)
    return OCCTRuntimeProbe(
        selected_module=selected,
        available=selected is not None,
        candidates=names,
    )
