import hashlib
from aias_level5_assurance import *
from aias_level5_assurance.reference import current_reference_assessment
from aias_level5_assurance.policy import Level5Policy
def evidence(classification):return [AssuranceEvidence(f"E-{classification}-{i}",c,classification,"2026-08-03T00:00:00+00:00","source",True,hashlib.sha256(f"{classification}{c}".encode()).hexdigest(),f"P-{i}") for i,c in enumerate(Level5Policy.REQUIRED_CRITERIA)]
def snapshot(days="2025-08-01T00:00:00+00:00",projects=12):return OrganizationalSnapshot("AIAS",days,"2026-08-03T00:00:00+00:00",projects,Level5Policy.REQUIRED_SYSTEMS,{"traceability_coverage":1.0,"quality_gate_pass_rate":.98,"verified_recovery_rate":1.0,"professional_review_compliance":1.0,"measured_time_reduction":.5,"improvement_actions_closed_rate":.9})
def audit():return AuditAttestation("AUD-1","Independent Assurance Ltd","Jane Auditor","ACC-1","2026-08-03T00:00:00+00:00","AIAS organization","LEVEL_5_CONFORMANT",0,"a"*64,True)
def test_current_aias_is_reference_level5_but_not_organizationally_audited():
 result=current_reference_assessment();assert result["level_5_reference"] and result["reference_capability_level"]==5 and not result["level_5_organizationally_audited"] and "independent_audit_missing" in result["gaps"]
def test_internal_or_reference_evidence_cannot_self_certify_organization():
 result=Level5Assessor().assess(snapshot(),evidence("REFERENCE_VALIDATION"),None);assert not result["level_5_organizationally_audited"] and len(result["production_criteria_missing"])==6
def test_complete_longitudinal_production_and_independent_audit_can_establish_level5():
 result=Level5Assessor().assess(snapshot(),evidence("REFERENCE_VALIDATION")+evidence("PRODUCTION_OBSERVATION"),audit());assert result["level_5_organizationally_audited"] and result["audited_organizational_level"]==5 and not result["gaps"]
def test_short_window_low_project_count_or_metric_failure_are_explicit():
 bad=OrganizationalSnapshot("AIAS","2026-07-01T00:00:00+00:00","2026-08-03T00:00:00+00:00",2,Level5Policy.REQUIRED_SYSTEMS,{"traceability_coverage":.5});result=Level5Assessor().assess(bad,evidence("REFERENCE_VALIDATION")+evidence("PRODUCTION_OBSERVATION"),audit());assert not result["level_5_organizationally_audited"] and any(x.startswith("observation_window") for x in result["gaps"]) and "traceability_coverage" in result["metric_failures"]
