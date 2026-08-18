"""Stable application portfolio models with explicit trust boundaries."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

APP_KINDS = frozenset({"DESKTOP", "WEB", "COMPANION", "SERVICE"})
TRUST_ZONES = frozenset({"LOCAL_TRUSTED", "INTERNAL_SERVICE", "PUBLIC_EDGE"})
LIFECYCLE_STATES = ("PROPOSED", "APPROVED", "VALIDATED", "RELEASED")


@dataclass(frozen=True, slots=True)
class ApplicationManifest:
    """Describe one governed AIAS application without claiming deployment."""

    app_id: str
    title: str
    kind: str
    trust_zone: str
    lifecycle: str = "PROPOSED"
    contract_version: str = "1.0.0"
    scopes: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    offline_supported: bool = False
    source_of_truth: bool = False
    evidence: tuple[str, ...] = ()

    def validate(self) -> None:
        """Reject ambiguous identities, unsupported zones and false truth ownership."""
        if not self.app_id.startswith("AIAS-APP-") or not self.app_id.isupper():
            raise ValueError("invalid_app_id")
        if self.kind not in APP_KINDS:
            raise ValueError("invalid_app_kind")
        if self.trust_zone not in TRUST_ZONES:
            raise ValueError("invalid_trust_zone")
        if self.lifecycle not in LIFECYCLE_STATES:
            raise ValueError("invalid_lifecycle")
        if self.source_of_truth:
            raise ValueError("applications_cannot_own_engineering_source_of_truth")
        if len(set(self.scopes)) != len(self.scopes):
            raise ValueError("duplicate_scope")

    def to_dict(self) -> dict:
        """Return a JSON-stable manifest representation."""
        self.validate()
        payload = asdict(self)
        for name in ("scopes", "capabilities", "evidence"):
            payload[name] = list(payload[name])
        return payload


@dataclass(frozen=True, slots=True)
class ContractDecision:
    """Record one allow-or-deny result suitable for audit evidence."""

    allowed: bool
    reason: str
    app_id: str
    operation: str
    project_id: str = ""
    evidence: dict = field(default_factory=dict)
