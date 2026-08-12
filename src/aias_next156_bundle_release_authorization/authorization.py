"""Internal authorization record for a verified local package."""

from __future__ import annotations

from typing import Any, Mapping


class BundleReleaseAuthorization:
    """Record an internal engineering decision without external authority."""

    def record(self, readiness: Mapping[str, Any]) -> dict[str, Any]:
        approved = readiness.get("readiness", {}).get("ready") is True
        return {
            "record": "AIAS-NEXT-156",
            "internally_authorized": approved,
            "external_authorization": False,
            "source": dict(readiness),
        }
