"""Stable local reporting for release candidates."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleaseCandidateReport:
    """Wrap a candidate descriptor without publishing it."""

    def generate(self, candidate: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "report": "AIAS-NEXT-149",
            "candidate": dict(candidate),
            "published": False,
        }
