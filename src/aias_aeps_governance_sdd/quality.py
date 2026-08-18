"""Constitutional specification, traceability, design and immediate-value gates."""
from .models import QualityGateResult, Specification
from .validators import SpecificationValidator
from .traceability import TraceabilityMatrix

class QualityGateEngine:
    """Evaluate mandatory SDD gates and expose a single completion predicate."""
    def evaluate(self, spec: Specification, traceability: TraceabilityMatrix) -> tuple[QualityGateResult, ...]:
        """Evaluate specification, traceability, ADR, architecture and value gates."""
        req_ids = [r.requirement_id for r in spec.requirements]
        issues = SpecificationValidator().validate(spec)
        coverage = traceability.coverage(req_ids)
        return (
            QualityGateResult("QG-SPEC", not issues, "Specification valid" if not issues else ";".join(issues)),
            QualityGateResult("QG-TRACE", coverage == 1.0, f"Traceability coverage={coverage:.2%}"),
            QualityGateResult("QG-ADR", bool(spec.adr_refs), "ADR linked" if spec.adr_refs else "No ADR linked"),
            QualityGateResult("QG-ARCH", bool(spec.architecture_refs), "Architecture linked" if spec.architecture_refs else "No architecture reference"),
            QualityGateResult("QG-VALUE", all(r.implements and r.tested_by for r in spec.requirements), "Immediate value path linked" if all(r.implements and r.tested_by for r in spec.requirements) else "Missing materialization path"),
        )

    def passed(self, spec: Specification, traceability: TraceabilityMatrix) -> bool:
        """Return true only when every mandatory constitutional gate passes."""
        return all(x.passed for x in self.evaluate(spec, traceability))
