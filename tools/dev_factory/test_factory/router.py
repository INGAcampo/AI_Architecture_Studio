"""Deterministic routing from changed paths to targeted AIAS test roots."""

from __future__ import annotations

from collections.abc import Iterable


ROUTES = (
    ("src/engines/geometry/occt/", "tests/devfactory/geometry_occt"),
    ("src/engines/bim/native_ifc/", "tests/devfactory/bim_native"),
    ("tools/dev_factory/test_factory/", "tests/devfactory/test_factory"),
)


def _normalize(path: str) -> str:
    return str(path).replace("\\", "/").lstrip("./").lower()


def classify_path(path: str) -> str:
    normalized = _normalize(path)
    for prefix, test_root in ROUTES:
        if normalized.startswith(prefix):
            return test_root
    return "UNROUTED"


def select_test_roots(paths: Iterable[str]) -> tuple[str, ...]:
    roots = {classify_path(path) for path in paths}
    roots.discard("UNROUTED")
    return tuple(sorted(roots))
