"""Stable reporting for internal authorization records."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleaseAuthorizationReport:
    """Wrap an internal authorization record without external claims."""

    def generate(self, record: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "report": "AIAS-NEXT-157",
            "authorization": dict(record),
            "external_authority": False,
        }
