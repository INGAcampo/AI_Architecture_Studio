"""Bidirectional identity and dry-run synchronization core for AIAS ↔ AutoCAD.

This stage deliberately performs no AutoCAD writes. It establishes stable
identity, fingerprints, change classification, conflict detection and sync plans.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Iterable


class SyncState(str, Enum):
    """Relationship state between AIAS and AutoCAD representations."""

    IN_SYNC = "in_sync"
    AIAS_CHANGED = "aias_changed"
    AUTOCAD_CHANGED = "autocad_changed"
    BOTH_CHANGED = "both_changed"
    MISSING_IN_AIAS = "missing_in_aias"
    MISSING_IN_AUTOCAD = "missing_in_autocad"


class SyncAction(str, Enum):
    """Dry-run action that a later write-enabled stage may execute."""

    NONE = "none"
    PUSH_TO_AUTOCAD = "push_to_autocad"
    PULL_FROM_AUTOCAD = "pull_from_autocad"
    CREATE_IN_AUTOCAD = "create_in_autocad"
    CREATE_IN_AIAS = "create_in_aias"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class ExternalIdentity:
    """Stable cross-system identity record."""

    aias_id: str
    autocad_handle: str
    document_key: str
    source: str = "AutoCAD"
    authority: str = "AutoCAD.Application.26"


@dataclass(frozen=True)
class SyncBaseline:
    """Last accepted fingerprints for both sides."""

    identity: ExternalIdentity
    aias_fingerprint: str
    autocad_fingerprint: str


@dataclass(frozen=True)
class SyncDecision:
    """Read-only synchronization decision."""

    identity: ExternalIdentity | None
    state: SyncState
    action: SyncAction
    reason: str
    aias_fingerprint: str | None = None
    autocad_fingerprint: str | None = None


def canonical_payload(entity: dict[str, Any]) -> dict[str, Any]:
    """Return deterministic geometry/property payload for synchronization."""
    ignored = {
        "selected",
        "highlighted",
        "hovered",
        "transient",
        "display_color",
        "screen_position",
    }
    return {
        str(k): entity[k]
        for k in sorted(entity)
        if k not in ignored
    }


def fingerprint(entity: dict[str, Any]) -> str:
    """Hash a normalized entity payload deterministically."""
    raw = json.dumps(
        canonical_payload(entity),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return sha256(raw).hexdigest()


def document_key(*, full_name: str | None, name: str | None = None) -> str:
    """Build a stable document identity from path/name evidence."""
    value = (full_name or name or "").strip().lower()
    if not value:
        raise ValueError("A document name or full path is required.")
    return sha256(value.encode("utf-8")).hexdigest()[:24]


class IdentityRegistry:
    """In-memory cross-system identity registry with collision protection."""

    def __init__(self) -> None:
        self._by_aias: dict[str, ExternalIdentity] = {}
        self._by_handle: dict[tuple[str, str], ExternalIdentity] = {}

    def bind(self, identity: ExternalIdentity) -> None:
        """Bind one AIAS ID to one AutoCAD handle in one document."""
        if not identity.aias_id:
            raise ValueError("AIAS ID cannot be empty.")
        if not identity.autocad_handle:
            raise ValueError("AutoCAD handle cannot be empty.")
        if not identity.document_key:
            raise ValueError("Document key cannot be empty.")

        existing_aias = self._by_aias.get(identity.aias_id)
        if existing_aias and existing_aias != identity:
            raise ValueError(f"AIAS ID already bound: {identity.aias_id}")

        hkey = (identity.document_key, identity.autocad_handle.upper())
        existing_handle = self._by_handle.get(hkey)
        if existing_handle and existing_handle != identity:
            raise ValueError(
                f"AutoCAD handle already bound in document: {identity.autocad_handle}"
            )

        self._by_aias[identity.aias_id] = identity
        self._by_handle[hkey] = identity

    def by_aias_id(self, aias_id: str) -> ExternalIdentity | None:
        """Resolve identity from AIAS ID."""
        return self._by_aias.get(aias_id)

    def by_autocad_handle(
        self, document_key_value: str, handle: str
    ) -> ExternalIdentity | None:
        """Resolve identity from AutoCAD document + handle."""
        return self._by_handle.get((document_key_value, handle.upper()))

    def all(self) -> tuple[ExternalIdentity, ...]:
        """Return all identities."""
        return tuple(self._by_aias.values())


class SyncPlanner:
    """Classify changes without mutating either application."""

    def decide(
        self,
        *,
        baseline: SyncBaseline | None,
        identity: ExternalIdentity | None,
        aias_entity: dict[str, Any] | None,
        autocad_entity: dict[str, Any] | None,
    ) -> SyncDecision:
        """Return a deterministic dry-run synchronization decision."""
        aias_fp = fingerprint(aias_entity) if aias_entity is not None else None
        acad_fp = fingerprint(autocad_entity) if autocad_entity is not None else None

        if aias_entity is None and autocad_entity is not None:
            return SyncDecision(
                identity=identity,
                state=SyncState.MISSING_IN_AIAS,
                action=SyncAction.CREATE_IN_AIAS,
                reason="Entity exists only in AutoCAD.",
                autocad_fingerprint=acad_fp,
            )

        if autocad_entity is None and aias_entity is not None:
            return SyncDecision(
                identity=identity,
                state=SyncState.MISSING_IN_AUTOCAD,
                action=SyncAction.CREATE_IN_AUTOCAD,
                reason="Entity exists only in AIAS.",
                aias_fingerprint=aias_fp,
            )

        if aias_entity is None and autocad_entity is None:
            raise ValueError("At least one side must contain an entity.")

        if baseline is None:
            if aias_fp == acad_fp:
                return SyncDecision(
                    identity=identity,
                    state=SyncState.IN_SYNC,
                    action=SyncAction.NONE,
                    reason="Both sides are equivalent; baseline may be created.",
                    aias_fingerprint=aias_fp,
                    autocad_fingerprint=acad_fp,
                )
            return SyncDecision(
                identity=identity,
                state=SyncState.BOTH_CHANGED,
                action=SyncAction.CONFLICT,
                reason="No baseline exists and both representations differ.",
                aias_fingerprint=aias_fp,
                autocad_fingerprint=acad_fp,
            )

        aias_changed = aias_fp != baseline.aias_fingerprint
        acad_changed = acad_fp != baseline.autocad_fingerprint

        if not aias_changed and not acad_changed:
            state, action, reason = (
                SyncState.IN_SYNC,
                SyncAction.NONE,
                "Neither representation changed from baseline.",
            )
        elif aias_changed and not acad_changed:
            state, action, reason = (
                SyncState.AIAS_CHANGED,
                SyncAction.PUSH_TO_AUTOCAD,
                "AIAS changed while AutoCAD remained at baseline.",
            )
        elif acad_changed and not aias_changed:
            state, action, reason = (
                SyncState.AUTOCAD_CHANGED,
                SyncAction.PULL_FROM_AUTOCAD,
                "AutoCAD changed while AIAS remained at baseline.",
            )
        else:
            state, action, reason = (
                SyncState.BOTH_CHANGED,
                SyncAction.CONFLICT,
                "Both AIAS and AutoCAD changed from the accepted baseline.",
            )

        return SyncDecision(
            identity=identity,
            state=state,
            action=action,
            reason=reason,
            aias_fingerprint=aias_fp,
            autocad_fingerprint=acad_fp,
        )


def build_baseline(
    identity: ExternalIdentity,
    aias_entity: dict[str, Any],
    autocad_entity: dict[str, Any],
) -> SyncBaseline:
    """Create a baseline from accepted equivalent/current representations."""
    return SyncBaseline(
        identity=identity,
        aias_fingerprint=fingerprint(aias_entity),
        autocad_fingerprint=fingerprint(autocad_entity),
    )


def serialize_baselines(baselines: Iterable[SyncBaseline]) -> list[dict[str, Any]]:
    """Serialize baselines for persistence without introducing storage coupling."""
    return [asdict(item) for item in baselines]
