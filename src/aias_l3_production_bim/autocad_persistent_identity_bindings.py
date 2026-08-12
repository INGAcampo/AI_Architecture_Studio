"""Public API for AIAS production BIM interoperability and transaction support."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple
import hashlib
import json
import os
import tempfile


SCHEMA = "aias.autocad.identity-bindings.v1"


@dataclass(frozen=True)
class IdentityBinding:
    """Represent IdentityBinding within the AIAS production BIM interoperability layer."""
    document_key: str
    aias_id: str
    autocad_handle: str
    fingerprint: str
    object_name: Optional[str] = None
    layer: Optional[str] = None

    @property
    def normalized_handle(self) -> str:
        """Execute the normalized handle operation for this interoperability component."""
        return self.autocad_handle.upper()

    def validate(self) -> None:
        """Execute the validate operation for this interoperability component."""
        if not self.document_key:
            raise ValueError("document_key is required.")
        if not self.autocad_handle:
            raise ValueError("autocad_handle is required.")
        if not self.aias_id:
            raise ValueError("aias_id is required.")
        expected = f"autocad:{self.document_key}:{self.normalized_handle}"
        if self.aias_id != expected:
            raise ValueError(
                f"Unstable AIAS ID: expected {expected!r}, got {self.aias_id!r}."
            )
        if not self.fingerprint:
            raise ValueError("fingerprint is required.")


@dataclass(frozen=True)
class ReconcileResult:
    """Represent ReconcileResult within the AIAS production BIM interoperability layer."""
    in_sync: Tuple[str, ...]
    missing_in_store: Tuple[str, ...]
    missing_in_source: Tuple[str, ...]
    fingerprint_mismatches: Tuple[str, ...]

    @property
    def clean(self) -> bool:
        """Execute the clean operation for this interoperability component."""
        return not (
            self.missing_in_store
            or self.missing_in_source
            or self.fingerprint_mismatches
        )


class PersistentIdentityBindingStore:
    """
    AIAS-side persistent AutoCAD identity registry.

    This store never calls AutoCAD. It persists only AIAS metadata and uses
    atomic replace semantics so a partial write cannot replace a valid registry.
    """

    def __init__(self, document_key: str) -> None:
        if not document_key:
            raise ValueError("document_key is required.")
        self.document_key = document_key
        self._by_handle: Dict[str, IdentityBinding] = {}
        self._handle_by_aias_id: Dict[str, str] = {}

    def __len__(self) -> int:
        return len(self._by_handle)

    def bindings(self) -> Tuple[IdentityBinding, ...]:
        """Execute the bindings operation for this interoperability component."""
        return tuple(self._by_handle[h] for h in sorted(self._by_handle))

    def get_by_handle(self, handle: str) -> Optional[IdentityBinding]:
        """Execute the get by handle operation for this interoperability component."""
        return self._by_handle.get(str(handle).upper())

    def get_by_aias_id(self, aias_id: str) -> Optional[IdentityBinding]:
        """Execute the get by aias id operation for this interoperability component."""
        h = self._handle_by_aias_id.get(aias_id)
        return self._by_handle.get(h) if h else None

    def bind(self, binding: IdentityBinding) -> None:
        """Execute the bind operation for this interoperability component."""
        binding.validate()
        if binding.document_key != self.document_key:
            raise ValueError("Binding document_key does not match store.")

        h = binding.normalized_handle
        existing_handle = self._handle_by_aias_id.get(binding.aias_id)
        if existing_handle is not None and existing_handle != h:
            raise ValueError(
                f"AIAS ID {binding.aias_id!r} is already bound to Handle {existing_handle}."
            )

        existing = self._by_handle.get(h)
        if existing is not None and existing.aias_id != binding.aias_id:
            raise ValueError(
                f"Handle {h} is already bound to AIAS ID {existing.aias_id!r}."
            )

        self._by_handle[h] = IdentityBinding(
            document_key=binding.document_key,
            aias_id=binding.aias_id,
            autocad_handle=h,
            fingerprint=binding.fingerprint,
            object_name=binding.object_name,
            layer=binding.layer,
        )
        self._handle_by_aias_id[binding.aias_id] = h

    def unbind_handle(self, handle: str) -> Optional[IdentityBinding]:
        """Execute the unbind handle operation for this interoperability component."""
        h = str(handle).upper()
        binding = self._by_handle.pop(h, None)
        if binding is not None:
            self._handle_by_aias_id.pop(binding.aias_id, None)
        return binding

    def reconcile(
        self,
        source_bindings: Iterable[IdentityBinding],
    ) -> ReconcileResult:
        """Execute the reconcile operation for this interoperability component."""
        source: Dict[str, IdentityBinding] = {}
        for binding in source_bindings:
            binding.validate()
            if binding.document_key != self.document_key:
                raise ValueError("Source binding document_key mismatch.")
            h = binding.normalized_handle
            if h in source:
                raise ValueError(f"Duplicate source Handle: {h}")
            source[h] = binding

        store_handles = set(self._by_handle)
        source_handles = set(source)

        missing_in_store = sorted(source_handles - store_handles)
        missing_in_source = sorted(store_handles - source_handles)
        common = store_handles & source_handles

        mismatches = sorted(
            h for h in common
            if self._by_handle[h].fingerprint != source[h].fingerprint
            or self._by_handle[h].aias_id != source[h].aias_id
        )
        in_sync = sorted(common - set(mismatches))

        return ReconcileResult(
            in_sync=tuple(in_sync),
            missing_in_store=tuple(missing_in_store),
            missing_in_source=tuple(missing_in_source),
            fingerprint_mismatches=tuple(mismatches),
        )

    def to_payload(self) -> Mapping[str, object]:
        """Execute the to payload operation for this interoperability component."""
        records = [asdict(b) for b in self.bindings()]
        payload = {
            "schema": SCHEMA,
            "document_key": self.document_key,
            "count": len(records),
            "records": records,
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return {
            **payload,
            "payload_sha256": hashlib.sha256(canonical).hexdigest(),
        }

    def save_atomic(self, path: Path) -> None:
        """Execute the save atomic operation for this interoperability component."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = self.to_payload()
        blob = (
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n"
        ).encode("utf-8")

        fd, tmp_name = tempfile.mkstemp(
            prefix=path.name + ".",
            suffix=".tmp",
            dir=str(path.parent),
        )
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(blob)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_name, path)
        except Exception:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass
            raise

    @classmethod
    def load(cls, path: Path) -> "PersistentIdentityBindingStore":
        """Execute the load operation for this interoperability component."""
        path = Path(path)
        payload = json.loads(path.read_text(encoding="utf-8-sig"))

        if payload.get("schema") != SCHEMA:
            raise ValueError("Unsupported identity binding schema.")

        document_key = payload.get("document_key")
        records = payload.get("records")
        if not isinstance(records, list):
            raise ValueError("Identity binding records must be a list.")

        count = payload.get("count")
        if count != len(records):
            raise ValueError("Identity binding count mismatch.")

        hash_payload = {
            "schema": payload["schema"],
            "document_key": document_key,
            "count": count,
            "records": records,
        }
        canonical = json.dumps(
            hash_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        expected_sha = hashlib.sha256(canonical).hexdigest()

        if payload.get("payload_sha256") != expected_sha:
            raise ValueError("Identity binding payload SHA-256 mismatch.")

        store = cls(str(document_key))
        for rec in records:
            store.bind(IdentityBinding(**rec))

        if len(store) != count:
            raise ValueError("Identity binding uniqueness/cardinality mismatch.")
        return store


def bindings_from_certified_baseline(
    baseline_payload: Mapping[str, object],
) -> List[IdentityBinding]:
    """Execute the bindings from certified baseline operation for AIAS production BIM interoperability."""
    document_key = str(baseline_payload.get("document_key") or "")
    if not document_key:
        raise ValueError("Certified baseline document_key is required.")

    result: List[IdentityBinding] = []
    seen_handles = set()
    seen_ids = set()

    for rec in baseline_payload.get("records", []):
        handle = str(rec.get("autocad_handle") or "").upper()
        aias_id = str(rec.get("aias_id") or "")
        fingerprint = str(rec.get("fingerprint") or "")
        mapped = rec.get("mapped") or {}

        if handle in seen_handles:
            raise ValueError(f"Duplicate baseline Handle: {handle}")
        if aias_id in seen_ids:
            raise ValueError(f"Duplicate baseline AIAS ID: {aias_id}")

        binding = IdentityBinding(
            document_key=document_key,
            aias_id=aias_id,
            autocad_handle=handle,
            fingerprint=fingerprint,
            object_name=mapped.get("object_name") or mapped.get("ObjectName"),
            layer=mapped.get("layer") or mapped.get("Layer"),
        )
        binding.validate()
        result.append(binding)
        seen_handles.add(handle)
        seen_ids.add(aias_id)

    return result
