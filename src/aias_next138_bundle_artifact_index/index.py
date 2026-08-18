"""Deterministic indexing of local bundle artifacts."""

from __future__ import annotations

from typing import Any, Iterable


class BundleArtifactIndex:
    """Create a stable ordinal index for artifact paths."""

    def build(self, artifacts: Iterable[str]) -> dict[str, Any]:
        items = sorted({str(artifact) for artifact in artifacts})
        return {
            "index": "AIAS-NEXT-138",
            "artifacts": [{"ordinal": position, "path": path} for position, path in enumerate(items, 1)],
            "count": len(items),
            "local_only": True,
        }
