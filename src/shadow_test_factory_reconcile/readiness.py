from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReconciliationReadiness:
    passed: bool
    ready_count: int
    manifest_missing: tuple[str,...]
    authority_violations: tuple[str,...]
    duplicate_megablocks: tuple[str,...]


def audit_queue_entries(entries) -> ReconciliationReadiness:
    seen=set()
    duplicates=[]
    missing=[]
    authority=[]

    values=tuple(entries)

    for item in values:
        name=str(item.get("megablock",""))

        if not name:
            duplicates.append("<blank>")
            continue

        if name in seen:
            duplicates.append(name)
        seen.add(name)

        manifest=str(item.get("package_manifest",""))
        if not manifest or not Path(manifest).is_file():
            missing.append(name)

        if bool(item.get("integration_authorized",False)):
            authority.append(name)

        if item.get("state")!="READY_FOR_RECONCILIATION":
            authority.append(name+":invalid_state")

    return ReconciliationReadiness(
        passed=not missing and not authority and not duplicates,
        ready_count=len(values),
        manifest_missing=tuple(sorted(set(missing))),
        authority_violations=tuple(sorted(set(authority))),
        duplicate_megablocks=tuple(sorted(set(duplicates))),
    )
