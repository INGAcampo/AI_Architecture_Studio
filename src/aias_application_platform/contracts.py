"""Versioned project and synchronization contracts shared by all AIAS apps."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field

from .models import ContractDecision
from .registry import ApplicationRegistry

PROJECT_ID = re.compile(r"^AIAS-PRJ-[A-Z0-9]{8,32}$")
SENSITIVITY = frozenset({"PUBLIC", "INTERNAL", "CONFIDENTIAL", "REGULATED"})


@dataclass(frozen=True, slots=True)
class ProjectEnvelope:
    """Reference the canonical project without copying its engineering truth."""

    project_id: str
    jurisdiction: str
    sensitivity: str
    revision: int
    canonical_uri: str
    schema_version: str = "1.0.0"
    capability_refs: tuple[str, ...] = ()
    metadata: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Validate identity, revision, jurisdiction and canonical URI boundaries."""
        if not PROJECT_ID.fullmatch(self.project_id):
            raise ValueError("invalid_project_id")
        if self.revision < 0:
            raise ValueError("invalid_revision")
        if self.sensitivity not in SENSITIVITY:
            raise ValueError("invalid_sensitivity")
        if not self.jurisdiction or self.jurisdiction.upper() != self.jurisdiction:
            raise ValueError("invalid_jurisdiction")
        if not self.canonical_uri.startswith("aias://projects/"):
            raise ValueError("noncanonical_project_uri")
        forbidden = {"password", "secret", "token", "private_key"}
        if forbidden & {str(key).lower() for key in self.metadata}:
            raise ValueError("secret_material_forbidden")

    def fingerprint(self) -> str:
        """Create a deterministic contract fingerprint for evidence and caching."""
        self.validate()
        payload = asdict(self)
        payload["capability_refs"] = list(self.capability_refs)
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class SyncRequest:
    """Request a projection synchronization against a known project revision."""

    app_id: str
    project: ProjectEnvelope
    operation: str
    expected_revision: int
    offline: bool = False


class ContractBroker:
    """Authorize scoped app access without replacing professional review or project truth."""

    OPERATIONS = {
        "project.read": "project:read",
        "project.propose": "project:propose",
        "evidence.append": "evidence:append",
        "learning.read": "learning:read",
    }

    def __init__(self, registry: ApplicationRegistry) -> None:
        self.registry = registry

    def authorize(self, request: SyncRequest) -> ContractDecision:
        """Fail closed on unknown scopes, stale writes, exposure and offline misuse."""
        request.project.validate()
        app = self.registry.get(request.app_id)
        required = self.OPERATIONS.get(request.operation)
        if not required:
            return self._deny(request, "unknown_operation")
        if app.lifecycle not in {"VALIDATED", "RELEASED"}:
            return self._deny(request, "application_not_validated")
        if required not in app.scopes:
            return self._deny(request, "scope_denied")
        if request.offline and not app.offline_supported:
            return self._deny(request, "offline_not_supported")
        if request.project.sensitivity == "REGULATED" and app.trust_zone == "PUBLIC_EDGE":
            return self._deny(request, "regulated_project_public_edge_denied")
        if request.operation != "project.read" and request.expected_revision != request.project.revision:
            return self._deny(request, "stale_revision")
        return ContractDecision(True, "authorized_projection_operation", app.app_id, request.operation, request.project.project_id, {"fingerprint": request.project.fingerprint()})

    @staticmethod
    def _deny(request: SyncRequest, reason: str) -> ContractDecision:
        return ContractDecision(False, reason, request.app_id, request.operation, request.project.project_id)
