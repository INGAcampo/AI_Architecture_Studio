"""Build a local release candidate from readiness evidence."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleaseCandidate:
    """Create a candidate descriptor without publishing it."""

    def create(self, readiness: Mapping[str, Any]) -> dict[str, Any]:
        ready = readiness.get("readiness", {}).get("ready") is True
        return {
            "candidate": "AIAS-NEXT-148",
            "eligible": ready,
            "source": dict(readiness),
            "published": False,
        }
