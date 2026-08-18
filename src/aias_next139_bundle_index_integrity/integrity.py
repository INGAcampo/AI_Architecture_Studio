"""Integrity checks for ordinal bundle indexes."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


class BundleIndexIntegrity:
    """Check that index ordinals are contiguous and paths are unique."""

    def check(self, artifacts: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
        items = list(artifacts)
        ordinals = [item.get("ordinal") for item in items]
        paths = [item.get("path") for item in items]
        contiguous = ordinals == list(range(1, len(items) + 1))
        unique_paths = len(paths) == len(set(paths))
        return {
            "integrity": "AIAS-NEXT-139",
            "valid": contiguous and unique_paths,
            "contiguous": contiguous,
            "unique_paths": unique_paths,
            "count": len(items),
            "external_attestation": False,
        }
