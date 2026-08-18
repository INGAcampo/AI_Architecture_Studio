"""Evidence-gated application registry for desktop, web and companion surfaces."""
from __future__ import annotations

from dataclasses import replace

from .models import ApplicationManifest, LIFECYCLE_STATES


class ApplicationRegistry:
    """Keep one immutable identity per app and enforce sequential maturity claims."""

    REQUIRED = {
        "APPROVED": "approval",
        "VALIDATED": "validation",
        "RELEASED": "release",
    }

    def __init__(self) -> None:
        self._apps: dict[str, ApplicationManifest] = {}

    def register(self, manifest: ApplicationManifest) -> ApplicationManifest:
        """Register an app once; conflicting reuse of its identifier fails closed."""
        manifest.validate()
        existing = self._apps.get(manifest.app_id)
        if existing and existing != manifest:
            raise ValueError("app_id_conflict")
        self._apps.setdefault(manifest.app_id, manifest)
        return self._apps[manifest.app_id]

    def get(self, app_id: str) -> ApplicationManifest:
        """Return a known application or reject the unknown caller."""
        if app_id not in self._apps:
            raise ValueError("unknown_application")
        return self._apps[app_id]

    def transition(self, app_id: str, target: str, evidence: dict) -> ApplicationManifest:
        """Advance one lifecycle state only when target evidence is explicit."""
        current = self.get(app_id)
        if target not in LIFECYCLE_STATES or LIFECYCLE_STATES.index(target) != LIFECYCLE_STATES.index(current.lifecycle) + 1:
            raise ValueError("invalid_lifecycle_transition")
        required = self.REQUIRED[target]
        if not evidence.get(required):
            raise ValueError(f"missing_gate_evidence:{required}")
        updated = replace(current, lifecycle=target, evidence=current.evidence + (str(evidence[required]),))
        self._apps[app_id] = updated
        return updated

    def public_inventory(self) -> list[dict]:
        """Expose manifests without credentials, tokens or user records."""
        return [self._apps[key].to_dict() for key in sorted(self._apps)]
