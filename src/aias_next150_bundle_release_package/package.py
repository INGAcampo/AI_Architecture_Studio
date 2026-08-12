"""Create a deterministic local release package descriptor."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


class BundleReleasePackage:
    """Group local release artifacts without publishing them."""

    def assemble(self, artifacts: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
        items = [dict(artifact) for artifact in artifacts]
        return {
            "package": "AIAS-NEXT-150",
            "artifacts": items,
            "count": len(items),
            "published": False,
        }
