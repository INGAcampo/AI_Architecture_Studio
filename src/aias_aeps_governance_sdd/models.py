"""Canonical requirement, specification and quality-gate contracts for AIAS SDD."""
from dataclasses import dataclass, field
from enum import Enum

class RequirementType(str, Enum):
    """Normative classification of functional, quality and constraint requirements."""
    FUNCTIONAL = "FUNCTIONAL"
    NON_FUNCTIONAL = "NON_FUNCTIONAL"
    CONSTRAINT = "CONSTRAINT"

class RequirementStatus(str, Enum):
    """Controlled requirement progression from draft through validated evidence."""
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    IMPLEMENTED = "IMPLEMENTED"
    VALIDATED = "VALIDATED"

@dataclass(slots=True)
class Requirement:
    """Normative need with rationale, acceptance, implementation and test links."""
    requirement_id: str
    title: str
    statement: str
    requirement_type: RequirementType
    status: RequirementStatus
    rationale: str
    acceptance_criteria: list[str] = field(default_factory=list)
    implements: list[str] = field(default_factory=list)
    tested_by: list[str] = field(default_factory=list)

@dataclass(slots=True)
class Specification:
    """Versioned development authority containing scope, requirements and design links."""
    specification_id: str
    title: str
    version: str
    purpose: str
    scope: str
    requirements: list[Requirement] = field(default_factory=list)
    architecture_refs: list[str] = field(default_factory=list)
    adr_refs: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

@dataclass(frozen=True, slots=True)
class QualityGateResult:
    """Immutable pass/fail decision and human-readable quality-gate evidence."""
    gate_id: str
    passed: bool
    message: str
