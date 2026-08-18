"""Reference capability and audited organizational maturity evaluation."""
from __future__ import annotations
from datetime import datetime,timezone
from .models import AssuranceEvidence,AuditAttestation,OrganizationalSnapshot
from .policy import Level5Policy
class Level5Assessor:
    """Assess without allowing tests or internal evidence to self-certify maturity."""
    def __init__(self,policy:Level5Policy|None=None):self.policy=policy or Level5Policy()
    def assess(self,snapshot:OrganizationalSnapshot,evidence:list[AssuranceEvidence],audit:AuditAttestation|None=None)->dict:
        """Return separate reference-capability and audited-organizational conclusions."""
        [item.validate() for item in evidence];systems_missing=sorted(set(self.policy.REQUIRED_SYSTEMS)-set(snapshot.operational_systems));criteria={criterion:[e for e in evidence if e.criterion_id==criterion] for criterion in self.policy.REQUIRED_CRITERIA};reference_missing=sorted(k for k,v in criteria.items() if not any(e.classification=="REFERENCE_VALIDATION" for e in v));reference_level5=not systems_missing and not reference_missing
        start=datetime.fromisoformat(snapshot.window_start);end=datetime.fromisoformat(snapshot.window_end);window_days=(end-start).days;production_missing=sorted(k for k,v in criteria.items() if not any(e.classification=="PRODUCTION_OBSERVATION" for e in v));metric_failures={key:{"actual":snapshot.metrics.get(key),"required":threshold} for key,threshold in self.policy.METRIC_THRESHOLDS.items() if snapshot.metrics.get(key) is None or snapshot.metrics[key]<threshold};audit_issues=[]
        if audit is None:audit_issues=["independent_audit_missing"]
        else:
            try:audit.validate()
            except ValueError as error:audit_issues=[str(error)]
            else:
                if audit.conclusion!="LEVEL_5_CONFORMANT":audit_issues.append("audit_conclusion_not_conformant")
                if audit.open_critical_findings:audit_issues.append("audit_critical_findings_open")
        gaps=[]
        if window_days<self.policy.MINIMUM_WINDOW_DAYS:gaps.append(f"observation_window_days:{window_days}<{self.policy.MINIMUM_WINDOW_DAYS}")
        if snapshot.completed_projects<self.policy.MINIMUM_PROJECTS:gaps.append(f"completed_projects:{snapshot.completed_projects}<{self.policy.MINIMUM_PROJECTS}")
        gaps += ["production_evidence_missing:"+x for x in production_missing]+["metric_below_threshold:"+x for x in sorted(metric_failures)]+audit_issues
        if snapshot.critical_findings:gaps.append("organizational_critical_findings_open")
        audited=reference_level5 and not gaps
        return {"assessment_id":f"L5-{snapshot.organization_id}-{snapshot.window_end}","reference_capability_level":5 if reference_level5 else None,"level_5_reference":reference_level5,"audited_organizational_level":5 if audited else None,"level_5_organizationally_audited":audited,"systems_missing":systems_missing,"reference_criteria_missing":reference_missing,"production_criteria_missing":production_missing,"observation_window_days":window_days,"completed_projects":snapshot.completed_projects,"metric_failures":metric_failures,"audit_present":audit is not None,"gaps":gaps,"warning":None if audited else "Level 5 organizational maturity is not established without longitudinal production evidence and an independent conformant audit."}
