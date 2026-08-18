from aias_integrated_management import CorrectiveAction, IntegratedManagementSystem, ManagementObjective, ManagementRisk


def system(tmp_path):
    return IntegratedManagementSystem(tmp_path / "ims")


def test_foundation_integrates_four_management_domains_without_claiming_certification(tmp_path):
    state = system(tmp_path).initialize()
    assert len(state["framework_targets"]) == 4 and len(state["control_families"]) == 7
    assert state["status"] == "IMPLEMENTED_FOUNDATION_NOT_CERTIFIED" and not state["certification_claim_permitted"]


def test_risk_register_is_owned_scored_and_domain_controlled(tmp_path):
    ims=system(tmp_path);row=ims.add_risk(ManagementRisk("IMSR-001","AI_MANAGEMENT","Unreviewed AI recommendation reaches a regulated deliverable",3,5,"AI Office","Require professional maker-checker gate"))
    assert row["score"]==15 and row["owner"]=="AI Office"


def test_objective_does_not_invent_observed_performance(tmp_path):
    ims=system(tmp_path);row=ims.add_objective(ManagementObjective("IMSO-001","QUALITY","Maintain governed traceability","traceability_coverage",0.0,0.95,"2027-08-03","Quality Office"))
    assert row["observed_value"] is None and row["target_achieved"] is None


def test_internal_audit_is_not_external_certification(tmp_path):
    row=system(tmp_path).schedule_internal_audit("IMS-AUD-001",("QUALITY","AI_MANAGEMENT"),"2026-10-01T00:00:00+00:00","Independent Internal Audit Function")
    assert row["classification"]=="INTERNAL_AUDIT_NOT_CERTIFICATION"


def test_management_review_and_corrective_action_are_traceable(tmp_path):
    ims=system(tmp_path);review=ims.record_management_review("IMS-MR-001",{"risk_summary":"current"},("Fund external gap assessment",),"2026-08-03T00:00:00+00:00");action=ims.add_corrective_action(CorrectiveAction("IMSCA-001","IMS-AUD-001","Missing licensed clause crosswalk","Normative copies not acquired","Acquire licensed standards","Compliance Office","2026-12-31"))
    assert len(review["evidence_sha256"])==64 and action["status"]=="OPEN"


def test_readiness_exposes_real_gaps_until_evidence_exists(tmp_path):
    result=system(tmp_path).readiness()
    assert result["foundation_implemented"] and not result["internal_readiness_complete"] and not result["externally_certified"]
