"""Syntactic and semantic validation for requirements and specifications."""
import re
from .models import Specification, Requirement, RequirementStatus

REQ_ID = re.compile(r"^REQ-\d{6}$")
SPEC_ID = re.compile(r"^SPEC-\d{6}$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

class RequirementValidator:
    """Enforce stable IDs, normative language, rationale and acceptance evidence."""
    def validate(self, req: Requirement) -> list[str]:
        """Collect requirement identity, language, rationale and acceptance issues."""
        issues = []
        if not REQ_ID.fullmatch(req.requirement_id):
            issues.append("invalid_requirement_id")
        if not req.title.strip():
            issues.append("missing_title")
        if "shall" not in req.statement.lower() and "deberá" not in req.statement.lower():
            issues.append("non_normative_statement")
        if not req.rationale.strip():
            issues.append("missing_rationale")
        if req.status in {RequirementStatus.APPROVED, RequirementStatus.IMPLEMENTED, RequirementStatus.VALIDATED} and not req.acceptance_criteria:
            issues.append("missing_acceptance_criteria")
        return issues

class SpecificationValidator:
    """Enforce identity, version, scope and valid nonempty requirement content."""
    def validate(self, spec: Specification) -> list[str]:
        """Collect specification metadata and nested requirement validation issues."""
        issues = []
        if not SPEC_ID.fullmatch(spec.specification_id):
            issues.append("invalid_specification_id")
        if not SEMVER.fullmatch(spec.version):
            issues.append("invalid_semver")
        if not spec.title.strip():
            issues.append("missing_title")
        if not spec.purpose.strip():
            issues.append("missing_purpose")
        if not spec.scope.strip():
            issues.append("missing_scope")
        if not spec.requirements:
            issues.append("missing_requirements")
        requirement_validator = RequirementValidator()
        for req in spec.requirements:
            for issue in requirement_validator.validate(req):
                issues.append(f"{req.requirement_id}:{issue}")
        return issues
