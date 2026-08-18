"""Deterministic manifest construction for local bundle artifacts."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


class BundleReleaseManifest:
    """Create a sorted manifest while preserving supplied hashes."""

    def build(self, artifacts: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
        items = sorted((dict(item) for item in artifacts), key=lambda item: str(item.get("path", "")))
        return {
            "manifest": "AIAS-NEXT-143",
            "artifacts": items,
            "count": len(items),
            "local_only": True,
        }
