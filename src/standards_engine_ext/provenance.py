from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class RulePackProvenance:
    source_name: str
    source_version: str
    jurisdiction: str
    effective_date: str | None = None
    source_uri: str | None = None


@dataclass(frozen=True)
class RulePack:
    pack_id: str
    version: str
    provenance: RulePackProvenance
    rule_ids: tuple[str, ...]
    content_sha256: str


def _canonical_payload(pack: RulePack) -> bytes:
    data={
        "pack_id":pack.pack_id,
        "version":pack.version,
        "provenance":{
            "source_name":pack.provenance.source_name,
            "source_version":pack.provenance.source_version,
            "jurisdiction":pack.provenance.jurisdiction,
            "effective_date":pack.provenance.effective_date,
            "source_uri":pack.provenance.source_uri,
        },
        "rule_ids":list(pack.rule_ids),
    }
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",",":"),
        ensure_ascii=True,
    ).encode("ascii")


def compute_rule_pack_sha256(pack: RulePack) -> str:
    return hashlib.sha256(_canonical_payload(pack)).hexdigest()


def verify_rule_pack(pack: RulePack) -> bool:
    if not pack.pack_id.strip():
        return False
    if not pack.version.strip():
        return False
    if not pack.provenance.source_name.strip():
        return False
    if not pack.provenance.source_version.strip():
        return False
    if not pack.provenance.jurisdiction.strip():
        return False
    if len(pack.content_sha256) != 64:
        return False
    if len(set(pack.rule_ids)) != len(pack.rule_ids):
        return False
    return compute_rule_pack_sha256(pack) == pack.content_sha256
