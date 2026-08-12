"""Vendor independence and competence screening for certification and CMMI appraisal."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderCandidate:
    """Represent one prospective external assurance provider without authorizing engagement."""
    provider_id: str
    provider_type: str
    legal_name: str
    accreditation_or_partner_reference: str
    public_verification_url: str
    proposed_scope: tuple[str, ...]
    independent: bool
    conflict_disclosed: bool
    high_maturity_lead_appraiser: bool = False
    aims_competence: bool = False


def evaluate_provider(candidate: ProviderCandidate) -> dict:
    """Screen minimum evidence while reserving selection and spending to authorized humans."""
    issues=[]
    if not candidate.provider_id.startswith("PROV-") or not all((candidate.legal_name,candidate.accreditation_or_partner_reference,candidate.public_verification_url)):issues.append("identity_or_credential_evidence_missing")
    if candidate.provider_type not in {"ISO_CERTIFICATION_BODY","CMMI_APPRAISAL_PROVIDER"}:issues.append("unsupported_provider_type")
    if not candidate.independent or not candidate.conflict_disclosed:issues.append("independence_not_established")
    if candidate.provider_type=="CMMI_APPRAISAL_PROVIDER" and not candidate.high_maturity_lead_appraiser:issues.append("high_maturity_lead_appraiser_missing")
    if candidate.provider_type=="ISO_CERTIFICATION_BODY" and "ISO-IEC-42001" in candidate.proposed_scope and not candidate.aims_competence:issues.append("aims_certification_competence_missing")
    return {"provider_id":candidate.provider_id,"eligible_for_due_diligence":not issues,"issues":issues,"selected":False,"contract_authorized":False,"spend_authorized":False}
