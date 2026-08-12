from aias_normative_access import ProviderCandidate,certification_scope,evaluate_provider,normative_assets


def test_registry_contains_all_approved_normative_assets_without_false_access():
    rows=normative_assets();assert len(rows)==6 and all(row["status"]=="NOT_ACQUIRED" and row["official_url"].startswith("https://") for row in rows)


def test_scope_excludes_professional_and_false_certification_claims():
    row=certification_scope();assert row["status"]=="DRAFT_FOR_EXTERNAL_SCOPING" and "licensed professional engineering approval" in row["excluded_claims"] and len(row["finalization_gates"])>=4


def test_cmmi_provider_requires_independence_and_high_maturity_appraiser():
    candidate=ProviderCandidate("PROV-001","CMMI_APPRAISAL_PROVIDER","Example","PARTNER-REF","https://example.invalid/verify",("CMMI-DEV-V3-ML5",),True,True,False)
    result=evaluate_provider(candidate);assert not result["eligible_for_due_diligence"] and "high_maturity_lead_appraiser_missing" in result["issues"] and not result["spend_authorized"]


def test_42001_provider_requires_aims_competence():
    candidate=ProviderCandidate("PROV-002","ISO_CERTIFICATION_BODY","Example","ACC-REF","https://example.invalid/verify",("ISO-IEC-42001",),True,True,aims_competence=False)
    assert "aims_certification_competence_missing" in evaluate_provider(candidate)["issues"]


def test_eligible_screening_never_selects_or_authorizes_contract():
    candidate=ProviderCandidate("PROV-003","ISO_CERTIFICATION_BODY","Example","ACC-REF","https://example.invalid/verify",("ISO-9001",),True,True)
    result=evaluate_provider(candidate);assert result["eligible_for_due_diligence"] and not result["selected"] and not result["contract_authorized"]
