"""Verification of local release manifest entries."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


class BundleManifestVerification:
    """Check that manifest entries have unique paths and non-empty hashes."""

    def verify(self, entries: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
        items = [dict(entry) for entry in entries]
        paths = [item.get("path") for item in items]
        hashes = [item.get("sha256") for item in items]
        valid = len(paths) == len(set(paths)) and all(bool(path) for path in paths) and all(bool(value) for value in hashes)
        return {
            "verification": "AIAS-NEXT-144",
            "valid": valid,
            "unique_paths": len(paths) == len(set(paths)),
            "hashes_present": all(bool(value) for value in hashes),
            "count": len(items),
            "external_attestation": False,
        }
