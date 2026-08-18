from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RulePackAdmission:
    accepted:bool
    reason:str

def evaluate_rule_pack_admission(
    *,
    source_evidence_accepted:bool,
    provenance_valid:bool,
    applicability_passed:bool,
    pack_hash_valid:bool,
)->RulePackAdmission:
    if not source_evidence_accepted:
        return RulePackAdmission(False,"source_evidence_rejected")
    if not provenance_valid:
        return RulePackAdmission(False,"provenance_invalid")
    if not applicability_passed:
        return RulePackAdmission(False,"not_applicable")
    if not pack_hash_valid:
        return RulePackAdmission(False,"pack_hash_invalid")
    return RulePackAdmission(True,"accepted")
