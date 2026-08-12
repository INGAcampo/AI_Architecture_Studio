"""Evidence-based five-level capability maturity assessment."""
from __future__ import annotations

LEVEL_CRITERIA = {
    1: ("repeatable_delivery",),
    2: ("repeatable_delivery", "traceability"),
    3: ("repeatable_delivery", "traceability", "automated_quality_gates"),
    4: ("repeatable_delivery", "traceability", "automated_quality_gates", "measured_acceleration"),
    5: ("repeatable_delivery", "traceability", "automated_quality_gates", "measured_acceleration", "continuous_improvement_loop"),
}

def assess(evidence: dict[str, bool]) -> dict:
    """Return the highest consecutive maturity level supported by evidence."""
    achieved = 0
    for level, criteria in LEVEL_CRITERIA.items():
        if all(evidence.get(item, False) for item in criteria): achieved = level
        else: break
    missing = [item for item in LEVEL_CRITERIA[5] if not evidence.get(item, False)]
    return {"level": achieved, "target_level": 5, "level_5_achieved": achieved == 5, "evidence": evidence, "missing_for_level_5": missing}
