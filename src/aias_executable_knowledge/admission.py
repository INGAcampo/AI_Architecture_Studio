"""License, provenance, execution and professional-boundary admission controls."""
from __future__ import annotations
from aias_aeks.models import KnowledgeUnit
from aias_aeks.validation import KnowledgeValidator
class KnowledgeAdmission:
 """Admit approved executable knowledge only with attributable reusable provenance."""
 def validate(self,unit:KnowledgeUnit)->list[str]:
  """Collect base-schema, license, provenance, execution and review-boundary issues."""
  issues=KnowledgeValidator().validate(unit);content=unit.content;license_info=content.get("license",{});provenance=content.get("provenance",{});execution=content.get("execution",{})
  if unit.status=="APPROVED" and not license_info.get("license_id"):issues.append("missing_license")
  if not license_info.get("redistribution_allowed"):issues.append("redistribution_not_allowed")
  if not provenance.get("publisher") or not provenance.get("source_uri"):issues.append("missing_provenance")
  if execution.get("mode")!="SAFE_DECLARATIVE_EXPRESSION" or execution.get("deterministic") is not True:issues.append("unsafe_execution_mode")
  if not unit.human_review_required:issues.append("missing_professional_review_boundary")
  if not unit.calculations:issues.append("missing_executable_calculation")
  return issues
