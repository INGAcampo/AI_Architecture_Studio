from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultQualityIssue:
    object_id: str
    code: str
    detail: str


def audit_result_records(records):
    issues=[]

    for record in records:
        object_id=str(getattr(record,"object_id",""))

        if not object_id.strip():
            issues.append(ResultQualityIssue(object_id,"MISSING_OBJECT_ID","object_id is blank"))

        value=float(getattr(record,"value",float("nan")))
        if not math.isfinite(value):
            issues.append(ResultQualityIssue(object_id,"NONFINITE_VALUE","result value is not finite"))

        unit=str(getattr(record,"unit",""))
        if not unit.strip():
            issues.append(ResultQualityIssue(object_id,"MISSING_UNIT","unit is blank"))

        case_name=str(getattr(record,"case_name",""))
        if not case_name.strip():
            issues.append(ResultQualityIssue(object_id,"MISSING_CASE","case_name is blank"))

    return tuple(issues)
