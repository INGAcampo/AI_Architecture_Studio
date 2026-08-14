from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ManifestVerification:
    passed: bool
    missing: tuple[str,...]
    mismatched: tuple[str,...]


def verify_manifest_entries(root, entries) -> ManifestVerification:
    base=Path(root)
    missing=[]
    mismatched=[]

    for item in entries:
        relative=str(item["path"])
        expected=str(item["sha256"]).lower()
        path=base/relative

        if not path.is_file():
            missing.append(relative)
            continue

        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=expected:
            mismatched.append(relative)

    return ManifestVerification(
        passed=not missing and not mismatched,
        missing=tuple(sorted(missing)),
        mismatched=tuple(sorted(mismatched)),
    )
