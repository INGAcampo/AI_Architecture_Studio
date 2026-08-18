"""Normative evidence and outcome policy for organizational Level 5 claims."""
from __future__ import annotations
class Level5Policy:
    """Define reference capability and independently audited maturity thresholds."""
    REQUIRED_SYSTEMS=("ACE","CNS","AEKS","EKG","DEV_PLATFORM","CAPABILITY_FACTORY","SECURITY_RECOVERY","PMO","UNIVERSITY","ATO","AEOS")
    REQUIRED_CRITERIA=("governance","repeatability","quantitative_management","continuous_improvement","resilience","professional_compliance")
    MINIMUM_WINDOW_DAYS=365;MINIMUM_PROJECTS=10
    METRIC_THRESHOLDS={"traceability_coverage":.95,"quality_gate_pass_rate":.95,"verified_recovery_rate":.95,"professional_review_compliance":1.0,"measured_time_reduction":.45,"improvement_actions_closed_rate":.8}
